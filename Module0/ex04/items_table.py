import psycopg2, os, sys
from pathlib import Path

def create_table(filename):

    dataname = Path(filename).stem
    create_cmd = '''CREATE TABLE ''' + dataname + ''' (
                product_id integer,
                category_id numeric(25,0),
                categry_code text,
                brand text)'''
    copy_cmd = """COPY """ + dataname + """ FROM '""" + filename + """' DELIMITER ',' CSV HEADER;"""

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
        cur.execute(create_cmd)
        cur.execute(copy_cmd)
        cur.close()
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('ERROR! Invalid number of arguments')
    create_table(sys.argv[1])

