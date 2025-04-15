import psycopg2, os, sys
from os import listdir
from os.path import isfile
sys.path.append('../ex02')
from table import create_tables

if __name__ == '__main__':

    if len(sys.argv) != 2:
        sys.exit('ERROR! Invalid number of arguments')
    path = sys.argv[1]
    files = [file for file in listdir(path) if isfile(path + file) and file.endswith(".csv")]

    for file in files:    
        create_tables(path + file)
