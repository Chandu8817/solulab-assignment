# Agent-1: Processes messages in the inbox every 10 seconds
import os
import random
import time
from queue import Queue
from blockchain.Blockchain import FROM_ADDRESS, get_token_balance, transfer_token
from dotenv import load_dotenv
load_dotenv()
running = True

# inbox and outbox queues
inbox = Queue()
outbox = Queue()
TARGET_ADDRESS = os.getenv('TARGET_ADDRESS') 

# list of words for generating messages
WORD_LIST = os.getenv('WORD_LIST') or ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"]
BALANCE_CHECK_TIME = os.getenv('BALANCE_CHECK_TIME') or 10
MESSAGE_GENERATE_TIME = os.getenv('MESSAGE_GENERATE_TIME') or 2
def agent_1(stop_event):
    while not stop_event.is_set():
        time.sleep(BALANCE_CHECK_TIME) 

        # Check the token balance
        get_token_balance(FROM_ADDRESS)

        # Process inbox messages
        while not inbox.empty():
            message = inbox.get()
            MESSAGE_WORD = os.getenv('MESSAGE_WORD') or "hello"
            CRYPTO_WORD = os.getenv('CRYPTO_WORD') or "crypto"


            if MESSAGE_WORD in message:
                print("Message with 'hello in outbox':", message)
            elif CRYPTO_WORD in message:
                transfer_token(TARGET_ADDRESS)
            outbox.put(message)

            # Check the stop event after processing each message
            if stop_event.is_set():
                break
# Agent-2 Generate message every 2 secs and puts them in Agent-1 inbox
def agent_2(stop_event):
    while not stop_event.is_set():
        time.sleep(MESSAGE_GENERATE_TIME)  
        
        message = f"{random.choice(WORD_LIST)} {random.choice(WORD_LIST)}"
        inbox.put(message) 
        print("Generated inbox message:", message)

