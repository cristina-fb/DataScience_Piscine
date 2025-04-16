import psycopg2, os, re
from pathlib import Path

def clean_tables(tablelist):
    tables = []
    for table in tablelist:
        if re.fullmatch('^data_202[0-9]_[a-z][a-z][a-z]', table[0]):
            tables += [table[0]]
    return tables

def get_join_cmd(tables):
    join_cmd = "CREATE TABLE customers AS"
    for i in range(0, len(tables)):
        join_cmd += " SELECT * FROM " + tables[i]
        if(i != len(tables) - 1):
            join_cmd += " UNION ALL"
    return join_cmd

def join_tables():
    get_tables_cmd = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"

    connection = None
    try:
        pgConnectionData = {
            'dbname': os.environ["POSTGRES_DB"],
            'user': os.environ["POSTGRES_USER"],
            'password': os.environ["POSTGRES_PASSWORD"],
            'port': os.environ["POSTGRES_PORT"],
            'host': os.environ["POSTGRES_HOST"]
        }
        connection = psycopg2.connect(**pgConnectionData)
        cur = connection.cursor()
        cur.execute(get_tables_cmd)
        tablelist = cur.fetchall()
        cur.execute(get_join_cmd(clean_tables(tablelist)))
        cur.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


if __name__ == '__main__':
    join_tables()

