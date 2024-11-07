import time
from web3 import Web3
import os

from blockchain.tokenAbi import token_abi
from dotenv import load_dotenv
load_dotenv()

ETH_NODE_URL = os.getenv("ETH_NODE_URL")   # tenderly node URL
TOKEN_CONTRACT_ADDRESS = os.getenv("TOKEN_CONTRACT_ADDRESS") 

web3 = Web3(Web3.HTTPProvider(ETH_NODE_URL))

FROM_ADDRESS = os.getenv("FROM_ADDRESS")  
GAS = os.getenv("GAS") or 200000
GAS_PRICE = os.getenv("GAS_PRICE") or "5"
DECIMAL = os.getenv("DECIMAL") or 6

token_contract = web3.eth.contract(address=TOKEN_CONTRACT_ADDRESS, abi=token_abi)

# get token balance
def get_token_balance(address):
    try:
        balance = token_contract.functions.balanceOf(address).call()
        adjusted_balance = balance / 10**DECIMAL  

        current_time = time.time()  
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(current_time))
        print("Time:", formatted_time)

        print(f"Token balance of {address}: {adjusted_balance}")
        return adjusted_balance

    except Exception as e:
        print(f"Error occurred while getting balance for address {address}: {e}")
        return None  # returning None in case of error

# transfer of token
def transfer_token(targetAddress):
    try:
        tokens = 1 * 10**DECIMAL  
        transaction = token_contract.functions.transfer(targetAddress, tokens).build_transaction({
            "from": FROM_ADDRESS,
            "nonce": web3.eth.get_transaction_count(FROM_ADDRESS),
            "gas": GAS,
            "gasPrice": web3.to_wei(GAS_PRICE, "gwei")     
        })

        signed_txn = web3.eth.account.sign_transaction(transaction, private_key=os.getenv("PRIVATE_KEY"))
        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        print(f"Simulating transfer of {tokens / 10**DECIMAL} token(s) from {FROM_ADDRESS} to {targetAddress}")
        print(f"Transaction Hash: {web3.to_hex(tx_hash)}")

    except Exception as e:
        print(f"Error occurred while transferring tokens from {FROM_ADDRESS} to {targetAddress}: {e}")
