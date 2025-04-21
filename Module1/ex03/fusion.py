import psycopg2, os

def remove_dups():
    fusion_cmd = """CREATE TABLE fusion_tmp AS
                    SELECT event_time, event_type, customers.product_id, price, user_id, user_session, category_id, category_code, brand
                    FROM customers
                    LEFT JOIN items ON customers.product_id = items.product_id AND items.category_id IS NOT NULL AND items.category_code IS NOT NULL AND items.brand IS NOT NULL;"""
    drop_table_cmd = """DROP TABLE customers"""
    rename_cmd = """ALTER TABLE fusion_tmp RENAME TO customers"""

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
        cur.execute(fusion_cmd)
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