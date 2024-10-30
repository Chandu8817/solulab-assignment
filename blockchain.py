from web3 import Web3
import os
from dotenv import load_dotenv
load_dotenv()

ETH_NODE_URL = os.getenv("ETH_NODE_URL")   # tenderly node URL
TOKEN_CONTRACT_ADDRESS = os.getenv("TOKEN_CONTRACT_ADDRESS") 

web3 = Web3(Web3.HTTPProvider(ETH_NODE_URL))

TOKEN_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "to", "type": "address"},
            {"name": "value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "from", "type": "address"},
            {"name": "to", "type": "address"},
            {"name": "value", "type": "uint256"}
        ],
        "name": "transferFrom",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    }
]

SOURCE_ADDRESS = os.getenv("SOURCE_ADDRESS")  
from_address = os.getenv("FROM_ADDRESS")  


token_contract = web3.eth.contract(address=TOKEN_CONTRACT_ADDRESS, abi=TOKEN_ABI)

# get token balance
def get_token_balance(address):
    balance = token_contract.functions.balanceOf(address).call()
    adjusted_balance = balance / 10**6  
    print(f"Token balance of {address}: {adjusted_balance}")
    return adjusted_balance  

# transfer of token
def transfer_token(targetAddress):

    tokens = 1 * 10**6  
    transaction = token_contract.functions.transferFrom(SOURCE_ADDRESS,targetAddress, tokens).build_transaction({
        "from": from_address,
        "nonce": web3.eth.get_transaction_count(from_address),
        "gas": 200000,
        "gasPrice": web3.to_wei("5", "gwei")  
    })

    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=os.getenv("PRIVATE_KEY"))
    web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    print(f"Simulating transfer of {tokens / 10**6} token(s) from {SOURCE_ADDRESS} to {targetAddress}")