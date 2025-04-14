import psycopg2, os
from os import listdir
from os.path import isfile, join
from table import create_tables

if __name__ == '__main__':

    mypath = "/home/customer/"
    files = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.endswith(".csv")]

    for file in files:    

        print(mypath+file)
        create_tables(mypath + file)
