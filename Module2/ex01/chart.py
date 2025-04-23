from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import psycopg2, os
import pandas as pd
import numpy as np

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
    month_sales = np.array(month_sales) / 1000000
    plt.grid(color='white', zorder=0, axis='y')
    plt.gca().set_facecolor('whitesmoke')
    plt.bar(months.keys(), month_sales, color='lightsteelblue', zorder=3)
    plt.xlabel('month')
    plt.ylabel('total sales in million of ₳')
    plt.savefig('monthly_sales.png', dpi=300)

def show_customers(sales, months):
    daily_data = sales.groupby(pd.Grouper(key='event_time', freq='D'))
    daily_customers = daily_data['user_id'].nunique()
    daily_sales = daily_data['price'].sum()
    plt.grid(color='white', zorder=0)
    plt.gca().set_facecolor('whitesmoke')
    plt.plot(daily_customers.index, daily_customers, color='royalblue', zorder=3)
    plt.xlabel('month')
    plt.ylabel('monetary value in ₳')
    plt.savefig('customers.png', dpi=300)

    plt.clf()
    plt.grid(color='white', zorder=0)
    plt.gca().set_facecolor('whitesmoke')
    plt.plot(daily_sales.index, daily_sales/daily_customers, color='lightsteelblue', zorder=3)
    plt.fill_between(daily_sales.index, daily_sales/daily_customers, color='lightsteelblue', zorder=3)
    plt.xlabel('month')
    plt.ylabel('average spend/customers in ₳')
    plt.savefig('average_spend.png', dpi=300)

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