import psycopg2

def create_tables(filename):

    tablename = filename[filename.rfind("/")+1:filename.find(".csv")]
    print(tablename)

    cmd_copy = """COPY """ + tablename + """ FROM '""" + filename + """' DELIMITER ',' CSV HEADER;"""
    print(cmd_copy)

    cmd_create = """
            CREATE TABLE """ + tablename + """ (
                event_time timestamp,
                event_type text,
                product_id integer,
                price float8,
                user_id bigint,
                user_session uuid
            )
            """

    conn = None
    try:
        pg_connection_dict = {
            'dbname': 'piscineds',
            'user': 'crisfern',
            'password': 'mysecretpassword',
            'port': 5432,
            'host': 'postgres'
        }
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**pg_connection_dict)
        cur = conn.cursor()
        # create table one by one
        #for command in commands:
        cur.execute(cmd_create)
        cur.execute(cmd_copy)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    #create_tables("/home/customer/data_2022_dec.csv")
    create_tables("/home/customer/data_2022_nov.csv")

