from functools import reduce
import hashlib as hl
from collections import OrderedDict
import json
import pickle

from hash_util import hash_string_256, hash_block
from block import Block
from transaction import Transaction

#Mining reward for miners(creating new block)
MINING_REWARD = 10


 # Initializing our blockchain list
blockchain = []

# Unhandled transactions
open_transactions = []

#We are the owner of blockchain, this is our identifier
owner = 'Eric'



def load_data():
    global blockchain
    global open_transactions
    try: 


        with open('blockchain.txt', mode = 'r') as f:
            file_content = f.readlines()
            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']
            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = []
            for block in blockchain:
                converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                updated_blockchain.append(updated_block)
                blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])

            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = Transaction(tx['sender'],tx['recipient'],tx['amount']) 
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions

    except (IOError,IndexError):
        #Starting block for the bc

        genesis_block = Block(0 ,'', [], 100, 0)

        # Initializing our blockchain list
        blockchain = [genesis_block]

        # Unhandled transactions
        open_transactions = []
    finally:
        print('Cleanup! ')
                



load_data()



def save_data():
    try:
        with open('blockchain.txt', mode = 'w') as f:
            saveable_chain = [block.__dict__ for block in [Block(block_el.index,block_el.previous_hash,[tx.__dict__ for tx in block_el.transactions] ,block_el.proof, block_el.timestamp) for block_el in blockchain]]
            f.write(json.dumps(saveable_chain))
            f.write('\n')
            saveable_tx = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(saveable_tx))
            # save_data = {
            #     'chain' : blockchain,
            #     'ot': open_transactions
            # }
            # f.write(pickle.dumps(save_data))
    except IOError:
        print('Saving failed! ')






def valid_proof(transactions, last_hash, proof):
    # Create a string with all the hash inputs
    guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
    
    #Hash the string
    # This is NOT the same hash as will be stored in the previous_hash
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2] == '00'




def proof_of_work():
    """ Generate a proof of work for open transactions."""
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    # Try different PoW numbers and return the frst valid one.
    proof = 0
    while not valid_proof(open_transactions,last_hash,proof):
        proof += 1

    return proof






def get_balance(participant):
    tx_sender = [[tx.amount for tx in block.transactions
     if tx.sender == participant] for block in blockchain]
    ## Fetch a list of all sent coin amounts for the given person
    ## This fetches sent amounts of open tranactions(to avoid double spending)
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum,tx_amount: tx_sum + sum(tx_amount) if len(tx_amount) > 0 else tx_sum + 0, tx_sender,0)
    tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in blockchain]
    amount_recieved = reduce(lambda tx_sum,tx_amount: tx_sum + sum(tx_amount) if len(tx_amount) > 0 else tx_sum +0, tx_recipient,0)
    ### Return total balance
    return amount_recieved - amount_sent

def get_last_blockchain():
    """Function definition for returning last value of current blockchain"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

def verify_transaction(transaction):
    sender_balance = get_balance(transaction.sender)
    return sender_balance >= transaction.amount



def add_transaction(recipient, sender = owner,amount = 1.0):
    """ Append a new value as well as the previous blockchain value to the current blockchain

    Arguments: sender: Sender of coins.
    recipient: Reciever of the coins. 
    amount: Amount of coins being sent.
    """

    # transaction = {
    # 'sender': sender,
    # 'recipient': recipient,
    # 'amount': amount 
    # }
    transaction = Transaction(sender,recipient,amount)
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        save_data()
        return True
    return False



def mine_block():
    """  Create a new block and add open transactions to it   """
    # Fetch the current last block of the blockchain
    last_block = blockchain[-1]
    # Hash the last block (=> to be able to compare it to the stored hash value)
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    #Miners should be rewarded
    # reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD
    # }
    reward_transaction = Transaction('MINING', owner, MINING_REWARD)



    # Copy transaction instead of manipuating the original open_transactions
    # This ensures that if for some reason the mining should fail, we dont reward the miner
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    blockchain.append(block)
    return True


def get_transaction_value():
    """" Returns the input of the user( new transaction amount) as a float value. """
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount please: '))
    return (tx_recipient,tx_amount)

def get_user_choice():
    user_input = input('Your choice ')
    return user_input

 #output blocks of blockchain
def print_blockchain_elements():      
    for blocks in blockchain:
        print('Outputting Block')
        print(blocks)
    else:
        print('-' * 20)

def verify_chain():
    """ Verify the current blockchain and return True if it's valid, false if it is not """
    for (index,block) in enumerate(blockchain):
        if index == 0:
            continue
        if block.previous_hash != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block.transactions[:-1] , block.previous_hash, block.proof):
            print('Proof of work is invalid')
            return False
    return True

def verify_transactions():
    """Verifies all open transactions."""
    return all([verify_transaction(tx) for tx in open_transactions])



waiting_for_input = True

while waiting_for_input:
    print('Please choose an option ')
    print('1: Add a new transaction value ')
    print('2: Mine new block ')
    print('3: Print current blockchain ')
    print('q: Press this to quit')
    user_choice = get_user_choice()


    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient,amount = tx_data
        #Add the transaction to the blockchain
        if add_transaction(recipient,amount = amount):
            print(open_transactions)
        else:
            print('Transaction Failed')
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice =='q':
        waiting_for_input = False
    else:
        print('Input was invalid, please enter valid value')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain ')
        break
    print('Balance of {} : {:6.2f}'.format('Eric',get_balance('Eric')))
else:
    print('User left! ')

print('Done!')
