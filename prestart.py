import sqlite3
from sqlite3 import Error
import os
import os.path
 
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print("Created new SQLLITE database with version {}".format(sqlite3.version))
        return conn
    except Error as e:
        print(e)


def sql_table(con):
 
    cursorObj = con.cursor()
 
    cursorObj.execute("CREATE TABLE hugs(id integer PRIMARY KEY, Sender text, Reciever text, NrHugs integer, Accepted integer, Rejected integer, NRG integer, blocked boolean)")
 
    con.commit()


if __name__ == '__main__':
    if(os.path.isfile('all.hugs')):
       print("No database detected, creating...")
       sc = create_connection("all.hugs")
       sql_table(sc)
       print("database created")
    token = input("Bot token: ")
    os.system("echo token = '{}' >> config.py".format(token))
