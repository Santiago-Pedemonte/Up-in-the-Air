import sqlite3
import random

def generate_transaction_number():
    db = Database()
    query = '''SELECT transaction_ID from transactions;'''
    query_result = db.cur.execute(query)
    transaction_ids = []
    for row in query_result:
        transaction_ids.append(row[0])
    m = 100000000
    transaction_num = random.choice([x for x in range(m) if x not in transaction_ids])
    return transaction_num


def generate_customer_ID():
    db = Database()
    query = '''SELECT customer_id from transactions;'''
    query_result = db.cur.execute(query)
    # db.connection.commit()
    # db.connection.row_factory = sqlite3.Row
    customer_id = []
    for row in query_result:
        customer_id.append(row[0])
    m = 100000000
    customer_num = random.choice([x for x in range(m) if x not in customer_id])
    return customer_num


def write_customer(transaction_id, first, last, flight_number, flight_delay,
                   calculated_payout, customer_id, flight_date):
    db = Database()

    db.cur.execute('''INSERT INTO transactions (transaction_ID, customer_first_name, customer_last_name,
                         flight_number, flight_delay_amt,
                           calculated_payout, customer_id, flight_date)
                          VALUES (?,?,?,?,?,?,?,?);''', (
        transaction_id, first, last, flight_number, flight_delay, calculated_payout,
        customer_id, flight_date))
    db.connection.commit()
    # # db.connection.row_factory = sqlite3.Row
    # customer_id = []
    # for row in query_result:
    #     customer_id.append(row[0])
    # m = max(customer_id)
    # customer_num = random.choice([x for x in range(m) if x not in customer_id])
    # return customer_num


def get_wallet_amount():
    db = Database()
    query = '''SELECT dollar_amount from wallet where customer_id = (SELECT MAX(customer_id) FROM wallet);'''
    query_result = db.cur.execute(query)
    transaction_ids = []
    for row in query_result:
        transaction_ids.append(row[0])
    wallet_amount = transaction_ids[0]
    return wallet_amount


def calculate_payout(delay_time):
    delay_rate = 25  # perhour
    if delay_time <= 0:
        return 0
    else:
        payout = delay_rate * delay_time/60
        return payout


def get_wallet_change(payout):
    new_value = get_wallet_amount() - payout
    return new_value


def update_insurance_wallet(dollar_amount, transactionID):
    db = Database()
    db.cur.execute('''insert into wallet ( dollar_amount, transactionID)
                    VALUES ( ?, ?);''', (dollar_amount, transactionID))
    db.connection.commit()
    
    
def show_wallet():
    db = Database()
    query = '''SELECT * FROM wallet;'''
    query_result = db.cur.execute(query)
    wallet_rows = []
    for row in query_result:
        wallet_rows.append(row)
    wallet_amount = wallet_rows
    return wallet_amount


def show_transactions():
    db = Database()
    query = '''SELECT * FROM transactions;'''
    query_result = db.cur.execute(query)
    transactions = []
    for row in query_result:
        transactions.append(row)
    transactions = transactions
    return transactions