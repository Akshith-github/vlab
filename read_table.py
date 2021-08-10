import sqlite3

def readSqliteTable():
    try:
        
        con = sqlite3.connect("data-dev.sqlite")
        print("Connected to SQLite")
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        # print(cursor.fetchall())
        tables= list(map(lambda x:x[0],cursor.fetchall()))
        print(*enumerate(tables),sep="\n")
        for table in tables:
            sqlite_select_query = """SELECT * from {0}""".format(table)
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            print("Total rows in {} are :  ".format(table), len(records))
            print("Printing each row")
            print(*records,sep="\n")
        """for row in records:
            print(row)
        cursor.close()"""
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        sqliteConnection=con
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

readSqliteTable()