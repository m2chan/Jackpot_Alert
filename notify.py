# Notifies subscribers using email and text based on their notification preferences

import sqlite3
from sqlite3 import Error
from lotto_data import retrieve_data

'''

Compare today's date with the lottery dates, if we are 1 day away, then query the database to pull all the people we should be texting/emailing
'''

def text_subscriber():
    '''
    Sends a text to all subscribers who should get notified
    '''
    pass

def email_subscriber():
    '''
    Sends an email to all subscribers who should get notified
    '''
    pass

def create_connection(db_file):
    '''
    Create a database connection to the SQLite subscribers database
    '''

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn
    
def lotto_649_query(conn, jackpot):
    '''
    Query subscribers who want to receive Lotto 649 notifications for jackpots at or below this week's jackpot
    '''

    curr = conn.cursor()
    curr.execute('SELECT * FROM subscribers WHERE lotto_649_threshold<=?', (jackpot,))

    rows = curr.fetchall()

    result_email = []
    result_phone = []
    
    for row in rows:
        result_email.append(row[1])
        result_phone.append(row[2])

    return result_email, result_phone

def lotto_max_query(conn, jackpot):
    '''
    Query subscribers who want to receive Lotto Max notifications for jackpots at or below this week's jackpot
    '''

    curr = conn.cursor()
    curr.execute('SELECT * FROM subscribers WHERE lotto_max_threshold<=?', (jackpot,))

    rows = curr.fetchall()

    result_email = []
    result_phone = []
    
    for row in rows:
        result_email.append(row[1])
        result_phone.append(row[2])

    return result_email, result_phone


def main():
    lottery_data = retrieve_data()
    current_lotto_649_jackpot = lottery_data['lotto_649']['jackpot']
    current_lotto_max_jackpot = lottery_data['lotto_max']['jackpot']
    
    database = 'subscribers.db'
    conn = create_connection(database)
    with conn:
        lotto_649_email, lotto_649_phone = lotto_649_query(conn, current_lotto_649_jackpot)
        lotto_max_email, lotto_max_phone = lotto_max_query(conn, current_lotto_max_jackpot)

    print(lotto_649_email)
    print(lotto_649_phone)
    print(lotto_max_email)
    print(lotto_max_phone)

if __name__ == '__main__':
    main()