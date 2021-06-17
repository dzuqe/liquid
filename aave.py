import json
import os
from web3 import Web3
from eth_abi import encode_single, encode_abi

# utils
gas_price=17
eth_price=2332

def display(accounts):
    print('account address                           ', '|', 
            'reserve underlying asset','|', 
            'health factor')

    for account in accounts:
            print(account['user']['id'], '|', 
                    account['reserve']['symbol'], '  |', 
                    account['totalBorrowsUSD'], '|', 
                    account['user']['healthFactor']
        )

def estimateTxFee(gas):
    print(((gas * gas_price)/1e9) * eth_price)

# ether opts
web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/' + os.environ['INFURA_API_KEY']))
key = os.environ['ETHEREUM_PRIVATE_KEY']
me = os.environ['ETHEREUM_ADDRESS']
bob = os.environ['BOB_ETHEREUM_ADDRESS']

WETH = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
DAI = os.environ['DAI_ADDR']
USDT = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
LINK = '0x514910771AF9Ca656af840dff83E8264EcF986CA'

def Dai():
    dss = json.load(open('/home/' + os.environ['USER'] + '/dev/dss/out/dapp.sol.json', 'r'))
    daiAbi = dss['contracts']['src/dai.sol:Dai']['abi']
    dai = web3.eth.contract(abi=daiAbi, address=os.environ['DAI_ADDR'])
    return dai

dai = Dai()

# aave options
def aave_abi(name):
    AAVE_PATH = '/home/' + os.environ['USER'] + '/dev/aave-v2/artifacts/contracts/interfaces'
    return json.load(open(f"{AAVE_PATH}/{name}.sol/{name}.json"))["abi"]

def aave():
    lpool_provider_addr = '0xB53C1a33016B2DC2fF3653530bfF1848a515c8c5'
    lpool_provider_abi = aave_abi('ILendingPoolAddressesProvider') 
    lpool_abi = aave_abi('ILendingPool')

    lpool_provider = web3.eth.contract(abi=aave_abi('ILendingPoolAddressesProvider'), address=lpool_provider_addr)
    lpool_addr = lpool_provider.functions.getLendingPool().call()
    lpool = web3.eth.contract(abi=aave_abi('ILendingPool'), address=lpool_addr)

    return (lpool, lpool_provider, lpool_addr)

lpool, lpool_provider, lpool_addr = aave()

accounts = json.load(open('liquidations.json', 'r'))['users']
low_health = [account for account in accounts 
                if float(account['user']['healthFactor']) > 0.5
                and float(account['totalBorrowsUSD']) > 500.0]

display(low_health)

# approve lending pool core address with dai contract
allowance = dai.functions.allowance(me, lpool_addr).call()
if allowance <= 0:
    print("not enough allowance you need to approve")

    approval = dai.functions.approve(lpool_addr, web3.toWei('1000000', 'ether')).buildTransaction({
        'gas': dai.functions.approve(lpool_addr, web3.toWei('1000000', 'ether')).estimateGas(),
        'gasPrice': web3.toWei(gas_price, 'gwei'),
        'nonce': web3.eth.getTransactionCount(me),
        'chainId': 1,
    })
    
    s_approval = web3.eth.account.sign_transaction(approval, private_key=key)
    web3.eth.sendRawTransaction(s_approval.rawTransaction)


# liquidate
#lpool.functions.liquidationCall(
#    WETH,               # collateral
#    DAI,                # debt
#    player2,            # user
#    (1<<256)-1,         # pay uint(-1)
#    True,               # receive underlying reserve token?
#    ).buildTransaction({
#        'gas': 1000000,
#        'gasPrice': web3.toWei(gas_price, 'gwei'),
#        'nonce': web3.eth.getTransactionCount(me),
#        'chainId': 1,
#})

#for acc in accounts:
#    if acc['reserve']['symbol'] in [TOKEN]:
#        player2 = web3.toChecksumAddress(acc['user']['id'])
#        debt = web3.toChecksumAddress(acc['reserve']['underlyingAsset'])
#
#        try:
#            estimateTxFee(lpool.functions.liquidationCall(
#                WETH,               # collateral
#                debt,
#                player2,            # user
#                (1<<256)-1          # pay uint(-1)
#                False,              # receive underlying reserve token?
#                ).estimateGas())
#
#        except:
#            print('failed to do liquidation')
