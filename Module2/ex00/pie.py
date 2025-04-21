from matplotlib import pyplot as plt
import numpy as np
import psycopg2, os

def get_data(event_type):
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
        for event in event_type:
            cmd = """SELECT COUNT(event_type) FROM customers WHERE event_type = '""" + event + """';"""
            cur.execute(cmd)
            n = cur.fetchall()
            data.append(n[0][0])
        cur.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
    return data

def show_pie(event_type, data):
    plt.pie(data, labels=event_type, autopct='%.1f%%')
    #plt.show()
    plt.savefig('pie.jpg')

if __name__ == '__main__':
    event_type = ['view', 'cart', 'remove_from_cart', 'purchase']
    data = get_data(event_type)
    show_pie(event_type, data)