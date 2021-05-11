#!/usr/bin/python3
import json
import mariadb
import time
import LiPe as lp

class dbcon:
    def __init__(self, dbname, dbadress, dbuser, password):
        self.i = 0
        self.db = mariadb.connect(
            user = dbuser,
            password = password,
            host = dbadress,
            port = 3306,
            database = dbname)
       
        

    def writecom(self, modul, state, message, exception):
        dbcursor = self.db.cursor()
        sql = "INSERT INTO serverlog (Modul, State, Message, Exception) VALUES (%s, %s, %s, %s)"
        val = (modul, state, message, exception)
        dbcursor.execute(sql, val)
        self.db.commit()
        return

    def prepareAndSelectLoggingTable(self, Tablename, nodesjs):
        cur = self.db.cursor()
        sql = "DROP TABLE IF EXISTS " + Tablename
        cur.execute(sql)
        sql = "CREATE TABLE " + Tablename + " (id INT AUTO_INCREMENT PRIMARY KEY)"   
        cur.execute(sql)
        sql = "ALTER TABLE " + Tablename + " ADD COLUMN " + "Time" + " TIMESTAMP"
        cur.execute(sql)
        for id in nodesjs:
            sql = "ALTER TABLE " + Tablename + " ADD COLUMN " + id + " FLOAT NOT NULL DEFAULT 0"
            cur.execute(sql)
        self.db.commit()
        #----------------------------------------------------------------------------------------
        sql = "INSERT INTO " + Tablename + " ("
        comma = False
        for id in nodesjs:
            if comma:
                sql = sql + ", "
            sql = sql + id
            comma = True
        comma = False 
        sqlpre = sql + ") VALUES ("
        return sqlpre

    def WriteActValues(self, sqlpre, actValues):
        comma = False
        cur = self.db.cursor()
        for value in actValues:        
            if comma:
                sql = sql + ", "
            else:
                sql = sqlpre
                comma = True 
            sql = sql + str(value)                   
        sql = sql + ")"
        cur.execute(sql)
        self.db.commit()

    def getLog(self):
        cur = self.db.cursor(dictionary=True)
        sql = "SELECT * FROM serverlog"
        cur.execute(sql)
        rows = cur.fetchall()
        self.db.commit()
        nesteddict = {}
        for row in rows:
            nesteddict[row["id"]] = row
        return nesteddict

    def deleteLog(self):
        cur = self.db.cursor()
        db = self.db
        sql = "DELETE FROM serverlog"
        cur.execute(sql)
        self.db.commit()
        return "Done"


    def getTables(self):
        cur = self.db.Cursor(dictionary=True)
        sql = "SHOW TABLES"
        cur.execute(sql)
        rows = cur.fetchall()
        nesteddict = {}
        i = 1
        for row in rows:
            nesteddict["Log "+ str(i)] = row["Tables_in_LiPe"]
            i += 1
        self.db.commit()
        return nesteddict

    def getTable(self, tablename):
        cur = self.dbcurdict
        sql = "SELECT * FROM " + tablename
        cur.execute(sql)
        rows = cur.fetchall()
        nesteddict = {}
        for row in rows:
            nesteddict[row["id"]] = row
        self.db.commit()
        return nesteddict

    def Test(self):
        result = "<h1>Dies ist ein Test</h1>"
        return(result)

    






