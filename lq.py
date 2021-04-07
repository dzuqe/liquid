import json
from web3 import Web3
from eth_abi import encode_single, encode_abi

def display(accounts):

    print('account address                           ', '|', 
            'reserve underlying asset','|', 
            'health factor')

    for account in accounts:
        print(account['user']['id'], '|', 
                account['reserve']['symbol'], '  |', 
                account['currentBorrowsUSD'], '|', 
                account['user']['healthFactor']
        )


def findAccount(addr, accounts):
    for account in accounts:
        if account['user']['id'] == addr:
            print(account['user'])
            return True
            break
        return False


def estimateTxFee(gas):
    gas_price=125
    eth_price=1750
    print(((gas * gas_price)/1000000000) * eth_price)

# ether opts
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/' + os.environ['INFURA_API_KEY']))
key = os.environ['ETHEREUM_PRIVATE_KEY']
me = os.environ['ETHEREUM_ADDRESS']
bob= os.environ['BOB_ETHEREUM_ADDRESS']

# setup dai
dss = json.load(open('/home/' + os.environ['USER'] + '/dev/dss/out/dapp.sol.json', 'r'))
daiAbi = dss['contracts']['src/dai.sol:Dai']['abi']
dai = web3.eth.contract(abi=daiAbi, address=os.environ['DAI_ADDR'])
daiAmountInWei = web3.toWei("1000", "ether")


# aave options
lpool_provider_addr = '0x24a42fD28C976A61Df5D00D0599C34c4f90748c8'
lpool_core_addr = '0x3dfd23A6c5E8BbcFc9581d2E864a68feb6a076d3'
lpool_addr = '0x398eC7346DcD622eDc5ae82352F02bE94C62d119'
receiveATokens = False

# setup lpool_provider
lpool_provider_abi = json.load(open('/home/' + os.environ['USER'] + '/dev/aave-protocol/build/contracts/LendingPoolAddressesProvider.json'))['abi']
lpool_abi = json.load(open('/home/' + os.environ['USER'] + '/dev/aave-protocol/build/contracts/LendingPool.json'))['abi']

lpool_provider = web3.eth.contract(abi=lpool_provider_abi, address=lpool_provider_addr)
lpool = web3.eth.contract(abi=lpool_abi, address=lpool_addr)



accounts = json.load(open('liquidations.json', 'r'))['data']
low_health = [account for account in accounts 
                if float(account['user']['healthFactor']) < 0.5
                and float(account['currentBorrowsUSD']) > 100.0]

display(low_health)

#findAccount('0x0bfe065d23f0dcfee35c96179e1e557724e3cde3', accounts)


# approve lending pool core address with dai contract
print('approval')
estimateTxFee(dai.functions.approve(lpool_core_addr, web3.toWei('1000000', 'ether')).estimateGas())
#approval = dai.functions.approve(lpool_core_addr, web3.toWei('1000000', 'ether')).buildTransaction({
#    'gas': dai.functions.approve(lpool_core_addr, web3.toWei('1000000', 'ether')).estimateGas(),
#    'gasPrice': web3.toWei('186', 'gwei'),
#    'nonce': web3.eth.getTransactionCount(me),
#    'chainId': 1,
#})
#
#s_approval = web3.eth.account.sign_transaction(approval, private_key=key)
#web3.eth.sendRawTransaction(s_approval.rawTransaction)


# make the deposit tx
#player2 = '0x0BfE065d23F0dCfEE35C96179e1e557724e3cdE3'
player2 = web3.toChecksumAddress('0x0bfe065d23f0dcfee35c96179e1e557724e3cde3')
WETH = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'

print()
print(player2)
user = lpool.functions.getUserAccountData(player2).call()
print(user)
estimateTxFee(lpool.functions.liquidationCall(
        os.environ['DAI_ADDR'],
        WETH,                       # the address of the reserve
        player2,                    # address
        web3.toWei('60', 'ether'),  # the amount of principal the liquidator wants to pay 
        receiveATokens,             # receive underlying reserve token?
        ).estimateGas())
