import numpy as np
import psycopg2, os
import matplotlib.pyplot as plt
import pandas as pd

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
        cmd = """SELECT event_time, price, user_id, user_session FROM customers WHERE event_type='purchase';"""
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
    data = pd.DataFrame(data, columns=['event_time', 'price', 'user_id','user_session'])
    price = data['price']
    baskets = data.groupby(['user_session', 'event_time']).agg({'price':'sum', 'user_id':'first'}).reset_index()
    baskets = baskets.groupby(['user_id']).agg({'price':'mean'}).reset_index()
    print('Count:' + str(len(price)))
    print('Mean:' + str(np.mean(price)))
    print('std:' + str(np.median(price)))
    print('Min:' + str(np.min(price)))
    print('Max:' + str(np.max(price)))
    print('25%:' + str(np.percentile(price, 25)))
    print('50%:' + str(np.percentile(price, 50)))
    print('75%:' + str(np.percentile(price, 75)))

    data = pd.DataFrame(data, columns=['price'])
    data.boxplot(vert=False, whiskerprops=dict(color='black'), medianprops=dict(color='black'), flierprops=dict(marker='D', markerfacecolor='gray', markersize=2), capprops=dict(color='black'), patch_artist=True)
    plt.grid(color='white', zorder=0)
    plt.gca().set_facecolor('whitesmoke')
    plt.savefig('boxplot.png', dpi=300)
    plt.clf()

    data.boxplot(vert=False, whiskerprops=dict(color='black'), medianprops=dict(color='black'), flierprops=dict(marker='D', markerfacecolor='gray', markersize=2), capprops=dict(color='black'), patch_artist=True)
    plt.grid(color='white', zorder=0)
    plt.gca().set_facecolor('whitesmoke')
    ax = plt.gca()
    ax.set_xlim([-5, 12])
    plt.savefig('boxplot_zoom.png', dpi=300)
    plt.clf()

    baskets = pd.DataFrame(baskets, columns=['price'])
    baskets.boxplot(vert=False, whiskerprops=dict(color='black'), medianprops=dict(color='black'), flierprops=dict(marker='D', markerfacecolor='gray', markersize=2), capprops=dict(color='black'), patch_artist=True)
    plt.grid(color='white', zorder=0)
    plt.gca().set_facecolor('whitesmoke')
    ax = plt.gca()
    ax.set_xlim([-5, 50])
    plt.savefig('boxplot_baskets.png', dpi=300)
    
