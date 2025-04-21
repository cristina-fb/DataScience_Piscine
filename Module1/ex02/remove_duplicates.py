import psycopg2, os, re
from pathlib import Path

def remove_dups():
    tmp_table_cmd = """CREATE TABLE unique_tmp AS
                        WITH rmv_temp AS( 
                        SELECT *, 
                        ROW_NUMBER() OVER (PARTITION BY event_type, product_id, price, user_id, user_session ORDER BY event_type, product_id, price, user_id, user_session, event_time ASC) AS RowNum,
                        LAG(event_time) OVER (ORDER BY event_type, product_id, price, user_id, user_session, event_time ASC) AS last_timestamp 
                        FROM customers)
                        SELECT event_time, event_type, product_id, price, user_id, user_session FROM rmv_temp WHERE 
                        RowNum = 1 OR ((RowNum > 1) AND (event_time > (last_timestamp + interval '1 second')))
                        ORDER BY event_time"""
    drop_table_cmd = """DROP TABLE customers"""
    rename_cmd = """ALTER TABLE unique_tmp RENAME TO customers"""

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
        cur.execute(tmp_table_cmd)
        cur.execute(drop_table_cmd)
        cur.execute(rename_cmd)
        cur.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


if __name__ == '__main__':
    remove_dups()

