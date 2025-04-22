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
    data = data.groupby(data['user_id']).sum()
    spend = []
    money = ['0', '50', '100', '150', '200', '250']
    for i in range(0,len(money)):
        spend.append(len(data[(data['price'] >= -25 + (50*i)) & (data['price'] < -25 + (50*(i+1)))]))
    plt.bar(money, spend, color='lightsteelblue', zorder=3) 
    plt.xlabel('monetary value in ₳')
    plt.ylabel('customers')
    plt.grid(color='white', zorder=0)
    plt.gca().set_facecolor('whitesmoke')
    plt.savefig('spend.png')

def show_freq_chart(data):
    freq = ['0', '10', '20', '30', '40']
    data = pd.DataFrame(data, columns=['price', 'user_id'])
    data = data.groupby(data['user_id']).count()
    freq_data = []
    for i in range(0,len(freq)):
        freq_data.append(len(data[(data['price'] >= 10*i) & (data['price'] < 10*(i+1))]))
    plt.bar(freq, freq_data, color='lightsteelblue', zorder=3)
    plt.grid(color='white', zorder=0)
    plt.gca().set_facecolor('whitesmoke')
    plt.xlabel('frequency')
    plt.ylabel('customers')
    plt.savefig('frequency.png')

if __name__ == '__main__':
    data = get_data()
    show_freq_chart(data)
    plt.clf()
    show_monetary_chart(data)