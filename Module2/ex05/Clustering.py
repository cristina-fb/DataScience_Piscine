from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2, os
import numpy as np
from datetime import datetime as dt

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
        cmd = """SELECT event_time, user_id, price FROM customers WHERE event_type = 'purchase'"""
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

    data = pd.DataFrame(get_data(), columns=['event_time', 'user_id', 'price'])
    
    data['event_time'] = pd.to_datetime(data['event_time'])
    data['event_time'] = (dt(2023,3,1,0,0,0).timestamp() - data['event_time'].astype(int).div(10**9))/(3600*24)
    model = data.groupby(['user_id']).agg({'price':'count', 'event_time':'last'}).reset_index()
    model = model.drop(['user_id'], axis=1)

    scaler = StandardScaler()
    model_scaled = scaler.fit_transform(model)
    kmeans = KMeans(n_clusters=3, random_state=42).fit(model_scaled)

    customers = []
    for n in range(3):
        customers.append((kmeans.labels_ == n).sum())
    barlist = plt.barh(['Inactive', 'New', 'Loyal'], customers)
    barlist[0].set_color('mediumaquamarine')
    barlist[1].set_color('lightsteelblue')
    barlist[2].set_color('plum')
    for index, value in enumerate(customers):
        plt.text(value, index, str(value))
    plt.xlabel('Number of customers')
    plt.savefig('Number_of_customers.png')
    plt.clf()

    LABEL_COLOR_MAP = {
        0: 'mediumaquamarine',
        1: 'lightsteelblue',
        2: 'plum'
    }
    label_color = [LABEL_COLOR_MAP[l] for l in kmeans.labels_]
    plt.xlabel('Last purchase (days)')
    plt.ylabel('Number of items purchased')
    plt.scatter(model['event_time'], model['price'], c=label_color, s=1, zorder=3)
    plt.grid(color='white', zorder=0)
    plt.gca().set_facecolor('whitesmoke')
    plt.savefig('Clusters.png')