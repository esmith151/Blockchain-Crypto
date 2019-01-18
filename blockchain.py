# Initializing our blockchain list
blockchain = []


def get_last_blockchain():
    """Function definition for returning last value of current blockchain"""
    return blockchain[-1]


def addVal(transactionNumber, last_transaction=[1]):
    """ Append a new value as well as the previous blockchain value to the current blockchain

    Arguments: transactionNumber: The amount that will be added
    last_transaction:  The last blockchain transaction (default is [1])
    """
    blockchain.append([last_transaction, transactionNumber])


def get_user_input():
    user_input = float(input('Your transaction amount please:'))
    return user_input

#Obtain first transaction amount and add to blockchain
tax_amount = get_user_input()
addVal(tax_amount)

#Obtain second transaction amount and add to blockchain
tax_amount = get_user_input()
addVal(last_transaction=get_last_blockchain(), transactionNumber=tax_amount)

#Obtain third transaction amount and add to blockchain
tax_amount = get_user_input()
addVal(tax_amount, get_last_blockchain())

for blocks in blockchain:
    print('Outputting Block')
    print(blocks)
