# Initializing our blockchain list
blockchain = []


def get_last_blockchain():
    """Function definition for returning last value of current blockchain"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def addVal(transactionNumber, last_transaction):
    """ Append a new value as well as the previous blockchain value to the current blockchain

    Arguments: transactionNumber: The amount that will be added
    last_transaction:  The last blockchain transaction (default is [1])
    """
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, transactionNumber])


def get_transaction_value():
    user_input = float(input('Your transaction amount please: '))
    return user_input

def get_user_choice():
    user_input = input('Your choice ')
    return user_input

 #output blocks of blockchain
def print_blockchain_elements():      
    for blocks in blockchain:
        print('Outputting Block')
        print(blocks)

def verify_chain():
    block_index = 0
    is_valid = True
    for block in blockchain:
        if block_index == 0:
            block_index += 1
            continue
        if block[0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
        block_index += 1
    return is_valid

while True:
    print('Please choose an option ')
    print('1: Add a new transaction value ')
    print('2: Print current blockchain ')
    print('h: Manipulate current blockchain ')
    print('q: Press this to quit')
    user_choice = get_user_choice()


    if user_choice == '1':
        tax_amount = get_transaction_value()
        addVal(tax_amount, get_last_blockchain())
    elif user_choice =='2':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]    
    elif user_choice =='q':
        break
    else:
        print('Input was invalid, please enter valid value')
    if not verify_chain():
        print('Invalid blockchain ')
        break
print('Done!')
