from __future__ import print_function

import cx_Oracle
import os

oh="D:/tools/Oracle/instantclient_12_2_x8664"
os.environ["ORACLE_HOME"]=oh
os.environ["PATH"]=oh+os.pathsep+os.environ["PATH"]
os.environ["NLS_LANG"]="AMERICAN_AMERICA.AL32UTF8"

def connectToOracle(url, username, password, mode=None):
    if mode is not None:
        connection = cx_Oracle.Connection (user=username, password=password, dsn=url, mode=mode)
    else:
        connection = cx_Oracle.Connection (user=username, password=password, dsn=url)
    return connection

def executeStmt(conn, stmt):
    if conn is not None and isinstance (conn, cx_Oracle.Connection):
        cur = conn.cursor()
        cur.execute(stmt)
    return cur

def describeCursor(cur):
    if cur is not None and isinstance (cur, cx_Oracle.Cursor):
        colnames = [row[0] for row in cur.description]
        coltypes = [row[1] for row in cur.description]
        coldisplay_sz = [row[2] for row in cur.description]
        colinternal_sz = [row[3] for row in cur.description]
        colprecision = [row[4] for row in cur.description]
        colscale = [row[5] for row in cur.description]
        colnullok = [row[6] for row in cur.description]
    print("Column names     : ",colnames)
    print("Column types     : ",coltypes)
    print("Display Size     : ",coldisplay_sz)
    print("Internal Size    : ",colinternal_sz)
    print("Column precision : ",colprecision)
    print("Column Scale     : ",colscale)
    print("Null OK?         : ",colnullok)


def printCursor(cur):
    if cur is not None and isinstance(cur, cx_Oracle.Cursor):
        for row in cur.fetchall():
            print(row)


# main
if __name__ == '__main__':
    c=cx_Oracle.Connection
    try:
        c=connectToOracle("192.168.99.2:1521/orcl","sys","oracle",mode=cx_Oracle.SYSDBA)
        curs=executeStmt(c,"select name,value from v$parameter where name like 'log_archive%' and name not like 'log_archive_dest%' ")
        #printCursor(curs)
        describeCursor(curs)
        curs.close()
    except cx_Oracle.DatabaseError as ex:
        err, =ex.args
        print("Error code    = ",err.code)
        print("Error Message = ",err.message)
        os._exit(1)
    c.close()
