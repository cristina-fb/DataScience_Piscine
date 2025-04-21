import numpy as np
import psycopg2, os
import matplotlib.pyplot as plt

def get_data():
    connection = None
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
        cmd = """SELECT price FROM customers WHERE event_type = 'purchase'"""
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

if __name__ == '__main__':
    data = get_data()
    print('Count:' + str(len(data)))
    print('Mean:' + str(np.mean(data)))
    print('std:' + str(np.median(data)))
    print('Min:' + str(np.min(data)))
    print('Max:' + str(np.max(data)))
    print('25%:' + str(np.percentile(data, 25)))
    print('50%:' + str(np.percentile(data, 50)))
    print('75%:' + str(np.percentile(data, 75)))

    plt.boxplot(data)
    plt.savefig('boxplot.png')