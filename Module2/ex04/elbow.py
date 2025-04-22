from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
import psycopg2, os

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
        cmd = """SELECT product_id, user_id FROM customers WHERE event_type = 'purchase'"""
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

    data = pd.DataFrame(get_data(), columns=['product_id', 'user_id'])
    model = data.groupby(data['product_id']).count()
    print(model)
    inertia = []
    for k in range(1, 10):
        kmeans = KMeans(n_clusters=k, random_state=42).fit(model)
        inertia.append(kmeans.inertia_)
    plt.title('The Elbow Method')
    plt.xlabel('Number of clusters')
    plt.plot(inertia, zorder=3)
    plt.grid(color='white', zorder=0)
    plt.gca().set_facecolor('whitesmoke')
    plt.savefig('elbow.png')