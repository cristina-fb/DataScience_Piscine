from matplotlib import pyplot as plt
import psycopg2, os
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
        cmd = """SELECT event_time, price, user_id FROM customers WHERE event_type = 'purchase'"""
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

def show_sales(sales, months):
    month_sales = []
    for month in months.values():
        month_sales.append(sales.loc[sales['event_time'].dt.month == month, 'price'].sum())
    print(month_sales)
    plt.bar(months.keys(), month_sales, color='b', alpha=0.42)
    plt.savefig('sales.png')

def show_customers(sales, months):
    daily_data = sales.groupby(pd.Grouper(key='event_time', freq='D'))
    daily_customers = daily_data['user_id'].nunique()
    daily_sales = daily_data['price'].sum()
    plt.plot(daily_customers.index, daily_customers, color='b', alpha=0.42)
    plt.savefig('customers.png')
    plt.clf()
    plt.plot(daily_sales.index, daily_sales/daily_customers, color='b', alpha=0.42)
    plt.fill_between(daily_sales.index, daily_sales/daily_customers, color='b', alpha=0.42)
    plt.savefig('sales2.png')

if __name__ == '__main__':
    months = {
        'Oct': 10,
        'Nov': 11,
        'Dec': 12,
        'Jan': 1,
        'Feb': 2
    }
    data = get_data()
    sales = pd.DataFrame(data, columns=['event_time', 'price', 'user_id'])
    show_sales(sales, months)
    plt.clf()
    show_customers(sales, months)