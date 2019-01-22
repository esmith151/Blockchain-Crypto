# Initializing our blockchain list
blockchain = []
open_transactions = []
owner = 'Eric'

def get_last_blockchain():
    """Function definition for returning last value of current blockchain"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender = owner,amount = 1.0):
    """ Append a new value as well as the previous blockchain value to the current blockchain

    Arguments: sender: Sender of coins
    recipient:  Reciever of the coins
    amount: amount of coins being sent
    """
    # Using dictionary to store transactions because of key value pair
    transaction = {
    'sender': sender,
    'recipient': recipient,
    'amount': amount }
    open_transactions.append(transaction)



def mine_block():
    pass


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
    # block_index = 0
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
    # for block in blockchain:
    #     if block_index == 0:
    #         block_index += 1
    #         continue
    #     if block[0] == blockchain[block_index - 1]:
    #         is_valid = True
    #     else:
    #         is_valid = False
    #         break
    #     block_index += 1
    return is_valid

waiting_for_input = True

while waiting_for_input:
    print('Please choose an option ')
    print('1: Add a new transaction value ')
    print('2: Print current blockchain ')
    print('h: Manipulate current blockchain ')
    print('q: Press this to quit')
    user_choice = get_user_choice()


    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient,amount = tx_data
        #Add the transaction to the blockchain
        add_transaction(recipient,amount = amount)
        print(open_transactions)
    elif user_choice =='2':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]    
    elif user_choice =='q':
        waiting_for_input = False
    else:
        print('Input was invalid, please enter valid value')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain ')
        break
else:
    print('User left! ')
print('Done!')
