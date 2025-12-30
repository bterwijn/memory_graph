import random

def make_change(amount, denominations):
    """ Returns a dict coin->count to make 'amount'. """
    change = {}
    for coin in denominations:
        if amount <= 0:
            break
        count, amount = divmod(amount, coin)
        if count > 0:
            change[coin] = count
    if amount != 0:
        raise ValueError("Cannot make exact change with these denominations.")
    return change

def show_change(change):
    print('coin  count')
    for coin, count in change.items():
        print(f'{coin:4}  {count:5}')

max_amount = 1000
amount = random.randrange(max_amount)
print('amount:', amount)

denominations = [50, 20, 10, 5, 2, 1]
change = make_change(amount, denominations)
print('change:', change)
show_change(change)
