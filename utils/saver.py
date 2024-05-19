import os
import psycopg2

USER_NAME = 'username'
PASS_WORD = 'password'
HOST = os.environ.get('HOST_POSTGREES')
PORT = os.environ.get('PORT_POSTGREES')

def save_correct_data(data):
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        dbname='postgres', user=USER_NAME, password=PASS_WORD
    )
    # Create table if it does not exist
    cur = conn.cursor()
    # Insert data into table
    for row in data:
        cur.execute('''
            INSERT INTO public.correct_user
            ("name", age, gender, email, phonenumber, address, creditcardid, weight, height)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (row.name, row.age, row.gender, row.email, row.phoneNumber, row.address, row.creditCardId, row.weight, row.height))
    # Commit changes and close connection
    conn.commit()
    cur.close()
    conn.close()

def save_incorrect_data(data):
    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        dbname='postgres', user=USER_NAME, password=PASS_WORD
    )
    # Create table if it does not exist
    cur = conn.cursor()
    # Insert data into table
    for row in data:
        cur.execute('''
            INSERT INTO public.incorrect_user
            ("name", age, gender, email, phonenumber, address, creditcardid, weight, height)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (row.name, row.age, row.gender, row.email, row.phoneNumber, row.address, row.creditCardId, row.weight, row.height))
    # Commit changes and close connection
    conn.commit()
    cur.close()
    conn.close()