# database structure
# <couple>;<numberofhugsglobal>;<blocked>;<#acceptedhugs>;<#rejectedhugs>;<#timeout>
# example
# C0der#9816-Redfire#9252;1337;false;1337;0;0

#!/usr/bin/env python3

import sqlite3
from sqlite3 import Error


def connect(file = 'all.hugs'):
    try:
        conn = sqlite3.connect(file)
        return conn
    except Error:
        return -1


def close_con(con):
    con.close()

def _sql_escape_string(strr):
    sr = str(strr)
    s = sr.replace("'", "''")
    return s 

def _sql_add_new_record(con, src, dst):
    curs = con.cursor()

    # Escape strings if user thinks he's smart
    srce = _sql_escape_string(src)
    dste = _sql_escape_string(dst)

    curs.execute("INSERT INTO hugs (Sender, Reciever, NrHugs, Accepted, Rejected, NRG, NrSlaps, blocked) VALUES('{}', '{}', 0, 0, 0, 0, 0, 'false')".format(srce, dste))
    print("SUCCESS: Added 1 entry")
    con.commit()

def _sql_check_if_record_exists(con, src, dst):
    cus = con.cursor()

    # Escape strings if user thinks he's smart
    srce = _sql_escape_string(src)
    dste = _sql_escape_string(dst)

    cus.execute("SELECT * FROM hugs WHERE Sender = '{}' AND Reciever = '{}'".format(srce, dste))
    r = cus.fetchall()

    if(len(r) == 1):
        print("SUCCESS: 1 entry found")
        return True
    elif(len(r) > 1):
        print("ERROR: FOUND DUPLICATES WITH SENDER {} AND RECIEVER {}".format(srce, dste))
        return True
    else:
        print("SUCCESS: 0 entries found")
        return False

def _sql_add_hug(con, src, dst, accepted):
    cur = con.cursor()

    # Escape strings if user thinks he's smart
    srce = _sql_escape_string(src)
    dste = _sql_escape_string(dst)

    # Change the SQL statement accordingly for acceptance
    if(accepted):
        cur.execute("UPDATE hugs SET NrHugs = NrHugs + 1, Accepted = Accepted + 1 WHERE Sender='{}' AND Reciever='{}'".format(srce, dste))
    else:
        cur.execute("UPDATE hugs SET NrHugs = NrHugs + 1, Rejected = Rejected + 1 WHERE Sender='{}' AND Reciever='{}'".format(srce, dste))
    con.commit()

def _sql_add_NRG(con, src, dst):
    cur = con.cursor()
    cur.execute("UPDATE hugs SET NrHugs = NrHugs + 1, NRG = NRG + 1 WHERE Sender='{}' AND Reciever='{}' ".format(src, dst))
    con.commit()

def _sql_upblockst(con, src, dst, blocked):

    # attach cursor
    cur = con.cursor()

    # Escape strings if user thinks he's smart
    srce = _sql_escape_string(src)
    dste = _sql_escape_string(dst)
    if(_sql_check_if_record_exists(con, srce, dste)):
        cur.execute("UPDATE hugs SET blocked = '{}' WHERE Sender='{}' AND Reciever='{}'".format(str(blocked), srce, dste))
        con.commit()
        cur.execute("UPDATE hugs SET blocked = '{}' WHERE Sender='{}' AND Reciever='{}'".format(str(blocked), dste, srce))
        con.commit()
    else:
        _sql_add_new_record(con, srce, dste)
        cur.execute("UPDATE hugs SET blocked = '{}' WHERE Sender='{}' AND Reciever='{}'".format(str(blocked), srce, dste))
        con.commit()
        cur.execute("UPDATE hugs SET blocked = '{}' WHERE Sender='{}' AND Reciever='{}'".format(str(blocked), dste, srce))
        con.commit()
    
def _sql_getinfo(con, src, dst):
    cur = con.cursor()

    # Escape strings if user thinks he's smart
    srce = _sql_escape_string(src)
    dste = _sql_escape_string(dst)

    cur.execute("SELECT NrHugs, Accepted, Rejected, NRG, NrSlaps FROM hugs WHERE Sender = '{}' AND Reciever='{}'".format(srce, dste))
    r = cur.fetchall()
    return r;

def _sql_add_slap(con, src, dst):
    # attach cursor
    cur = con.cursor()

    # Escape strings if user thinks he's smart
    srce = _sql_escape_string(src)
    dste = _sql_escape_string(dst)
    if(_sql_check_if_record_exists(con, srce, dste)):
        cur.execute("UPDATE hugs SET NrSlaps = NrSlaps + 1 WHERE Sender='{}' AND Reciever='{}'".format(srce, dste))
        con.commit()
    else:
        _sql_add_new_record(con, srce, dste)
        cur.execute("UPDATE hugs SET NrSlaps = NrSlaps + 1 WHERE Sender='{}' AND Reciever='{}'".format(srce, dste))
        con.commit()

def _sql_getblockst(con, src, dst):
    cur = con.cursor()

    # Escape strings if user thinks he's smart
    srce = _sql_escape_string(src)
    dste = _sql_escape_string(dst)


    cur.execute("SELECT blocked FROM hugs WHERE Sender = '{}' AND Reciever = '{}'".format(srce, dste))
    r = cur.fetchall()
    return r;



def RecordHug(src, dst, accepted):
    c = connect()
    r = _sql_check_if_record_exists(c, src, dst)
    if(r):
        _sql_add_hug(c, src, dst, accepted)
    elif(r == False):
        _sql_add_new_record(c, src, dst)
        _sql_add_hug(c, src, dst, accepted)
    
    close_con(c)

def RecordNRG(src, dst):
    c = connect()
    _sql_add_NRG(c, src, dst)
    close_con(c)

def blockUsr(src, dst):
    c = connect()
    _sql_upblockst(c, src, dst, True)
    close_con(c)

def unblockUsr(src, dst):
    c = connect()
    _sql_upblockst(c, src, dst, False)
    close_con(c)

def getinfo(src, dst):
    c = connect()
    r = _sql_getinfo(c, src, dst)
    close_con(c)
    return r

def getblockst(src, dst):
    c = connect()
    r = _sql_getblockst(c, src, dst)
    
    if(len(r) < 1):
        return False
    
    re = r[0]
    close_con(c)
    if(re[0] == 'false'):
        return False

    elif(re[0] == 'False'):
        return False

    elif(re[0] == 'true'):
        return True
    elif(re[0] == 'True'):
        return True


    return False

def recordslap(src, dst):
    c = connect()
    _sql_add_slap(c, src, dst)
    close_con(c)