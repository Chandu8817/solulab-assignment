# Agent-1: Processes messages in the inbox every 10 seconds
import random
import time
from queue import Queue

from blockchain import SOURCE_ADDRESS, get_token_balance, transfer_token
running = True

# inbox and outbox queues
inbox = Queue()
outbox = Queue()
targetAddress = '0xFa7e2322AE858d58CDb7C4D8e2687c447d08c231'

# list of words for generating messages
words = ["hello", "sun", "world", "space", "moon", "crypto", "sky", "ocean", "universe", "human"]

def agent_1(stop_event):
    while not stop_event.is_set():
        time.sleep(10) 

        # Check the token balance
        get_token_balance(SOURCE_ADDRESS)

        # Process inbox messages
        while not inbox.empty():
            message = inbox.get()

            if "hello" in message:
                print("Message with 'hello in outbox':", message)
            elif "crypto" in message:
                transfer_token(targetAddress)
            outbox.put(message)

            # Check the stop event after processing each message
            if stop_event.is_set():
                break
# Agent-2 Generate message every 2 secs and puts them in Agent-1 inbox
def agent_2(stop_event):
    while not stop_event.is_set():
        time.sleep(2)  
        
        message = f"{random.choice(words)} {random.choice(words)}"
        inbox.put(message) 
        print("Generated inbox message:", message)

