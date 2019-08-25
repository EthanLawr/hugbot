import config
import sqlite3
import discord

def connect(file = 'all.hugs'):
    try:
        conn = sqlite3.connect(file)
        return conn
    except Error:
        return -1


def close_con(con):
    con.close()


def _canupdate():
    if hasattr(config, 'version'):
        return True
    if (config.version < 0.91):
        return True
    elif(config.version >= 0.91):
        return False
    return False

def _changedatabase():
    
    c = connect()
    cu = c.cursor()
    if(c == -1):
        print('could not connect to database')
        exit(1)

    cu.execute('ALTER TABLE hugs ADD NrSlaps integer')
    c.commit()

    print('We\'ve moved to IDs, others are now invalid')


if __name__ == '__main__':
    if(_canupdate):
        _changedatabase()
        config.version = 0.91
    else:
        print('already updated')
    
    
