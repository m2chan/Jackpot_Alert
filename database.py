# Create subscribers database

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    '''
    Create a database connection to the SQLite subscribers database
    
    Input arguments:
        db_file: Database name we are connecting to
    '''

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    '''
    Creates a table to store subscriber data and preferences.

    Input arguments:
        conn: SQLite3 connection object
        create_table_sql: Create table statement
    '''

    try: 
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_subscriber(conn, subscriber_data):
    '''
    Adds a new subscriber to the database

    Input arguments: 
        conn: SQLite3 connection object
        subscriber: Subscriber data to insert
    '''

    sql = ''' INSERT INTO subscribers(email,phone,lotto_649,lotto_649_threshold,lotto_max,lotto_max_threshold,lucky_numbers)
              VALUES(?,?,?,?,?,?,?)
    '''

    cur = conn.cursor()
    cur.execute(sql, subscriber_data)
    conn.commit()
    return cur.lastrowid

if __name__ == '__main__':
    database = 'subscribers.db'
    
    # Initialize database with these rows
    sql_create_subscribers_table = ''' CREATE TABLE IF NOT EXISTS subscribers (
                                            id integer PRIMARY KEY,
                                            email text,
                                            phone text,
                                            lotto_649 integer,
                                            lotto_649_threshold integer,
                                            lotto_max integer,
                                            lotto_max_threshold integer,
                                            lucky_numbers integer                                                                                  
    )
    '''
    
    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_subscribers_table)
    
    with conn:

        sub_1 = ('name1@email.com', '4162003000', 1, 5, 1, 30, 1)
        sub_2 = ('name2@email.com', '4161002000', 1, 10, 1, 50, 1)

        create_subscriber(conn, sub_1)
        create_subscriber(conn, sub_2)

