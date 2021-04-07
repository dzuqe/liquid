from web3 import Web3
from dydx3 import Client
import os

api_cred = {
    'secret': os.environ['DYDX_SECRET'],
    'key': os.environ['DYDX_KEY'],
    'passphrase': os.environ['DYDX_PASSPHRASE']
}

client = Client(
    host='https://api.dydx.exchange',
    web3=Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/' + os.environ['INFURA_API_KEY'])),
    #stark_private_key=os.environ['STARK_PRIVATE_KEY'],
    stark_public_key=os.environ['STARK_PUBLIC_KEY'],
    api_key_credentials=api_cred,
    eth_private_key=os.environ['ETHEREUM_PRIVATE_KEY'],
    default_ethereum_address=os.environ['ETHEREUM_ADDRESS']
)


