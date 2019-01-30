# Initializing our blockchain list
MINING_REWARD = 10

genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
    }
blockchain = [genesis_block]
open_transactions = []
owner = 'Eric'
participants = {'Eric'}

def hash_block(block):
    return '-'.join([str(block[key]) for key in block])

def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
     
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent+= tx[0] 
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_recieved = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_recieved+= tx[0] 
    return amount_recieved - amount_sent

def get_last_blockchain():
    """Function definition for returning last value of current blockchain"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']



def add_transaction(recipient, sender = owner,amount = 1.0):
    """ Append a new value as well as the previous blockchain value to the current blockchain

    Arguments: sender: Sender of coins.
    recipient: Reciever of the coins. 
    amount: Amount of coins being sent.
    """
    # Using dictionary to store transactions because of key value pair
    transaction = {
    'sender': sender,
    'recipient': recipient,
    'amount': amount }
    
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False



def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    open_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': open_transactions
        }
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
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
    return True


waiting_for_input = True

while waiting_for_input:
    print('Please choose an option ')
    print('1: Add a new transaction value ')
    print('2: Mine new block ')
    print('3: Print current blockchain ')
    print('4: Print participant list ')
    print('h: Manipulate current blockchain ')
    print('q: Press this to quit')
    user_choice = get_user_choice()


    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient,amount = tx_data
        #Add the transaction to the blockchain
        add_transaction(recipient,amount = amount)
        print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
            'previous_hash': '',
            'index': 0,
            'transactions': [{'sender': 'Chris', 'recipient': 'Eric', 'amount': 100.0 }]
        }   
    elif user_choice =='q':
        waiting_for_input = False
    else:
        print('Input was invalid, please enter valid value')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain ')
        break
    print(get_balance('Eric'))
else:
    print('User left! ')

print('Done!')
