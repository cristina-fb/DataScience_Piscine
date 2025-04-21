import psycopg2, os
import matplotlib.pyplot as plt
import pandas as pd

def get_data():
    connection = None
    data = []
    try:
        pgConnectionData = {
            'dbname': os.environ['POSTGRES_DB'],
            'user': os.environ['POSTGRES_USER'],
            'password': os.environ['POSTGRES_PASSWORD'],
            'port': os.environ['POSTGRES_PORT'],
            'host': os.environ['POSTGRES_HOST']
        }
        connection = psycopg2.connect(**pgConnectionData)
        cur = connection.cursor()
        cmd = """SELECT price, user_id FROM customers WHERE event_type = 'purchase'"""
        cur.execute(cmd)
        data = cur.fetchall()
        cur.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
    return data

def show_monetary_chart(data):
    data = pd.DataFrame(data, columns=['price', 'user_id'])
    print(data['user_id'])
    data = data.groupby(data['user_id'])
    money = [0, 50, 100, 150, 200]
    plt.bar(data, money)
    plt.xlabel('monetary value in ₳')
    plt.ylabel('customers')
    plt.show()
    plt.savefig('bar.png')

def show_freq_chart(data):
    freq = [0, 10, 20, 30, 40]
    data = get_freq_data(freq)
    plt.bar(data, freq)
    plt.xlabel('frequency')
    plt.ylabel('customers')
    plt.show()


if __name__ == '__main__':
    data = get_data()
    #show_freq_chart(data)
    show_monetary_chart(data)