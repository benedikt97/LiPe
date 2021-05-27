#!/usr/bin/python3
import mariadb
import time


class dbcon:
    def __init__(self, dbname, dbadress, dbuser, password):
        self.db = mariadb.connect(
            user = dbuser,
            password = password,
            host = dbadress,
            port = 3306,
            database = dbname)
       
        

    def writecom(self, modul, state, message, exception):
        cur = self.db.cursor()
        sql = "INSERT INTO serverlog (Modul, State, Message, Exception) VALUES (%s, %s, %s, %s)"
        val = (modul, state, message, exception)
        cur.execute(sql, val)
        cur.close()
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
        cur.close()
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
            sql = sql + str(actValues[value])                   
        sql = sql + ")"
        print(sql)
        cur.execute(sql)
        cur.close()
        self.db.commit()
        

    def getLog(self):
        cur = self.db.cursor(dictionary=True)
        sql = "SELECT * FROM serverlog"
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        self.db.commit()
        nesteddict = {}
        x = 0
        for row in rows:
            nesteddict[x] = row
            x = x + 1
        return nesteddict

    def deleteLog(self):
        cur = self.db.cursor()
        sql = "DELETE FROM serverlog"
        cur.execute(sql)
        cur.close()
        self.db.commit()
        return "Done"

    def deleteTable(self, name):
        cur = self.db.cursor()
        sql = "DELETE FROM " + name
        cur.execute(sql)
        cur.close()
        self.db.commit()
        return "Done"



    def getTables(self):
        cur = self.db.cursor(dictionary=True)
        sql = "SHOW TABLES"
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        nesteddict = {}
        i = 1
        for row in rows:
            nesteddict["Log "+ str(i)] = row["Tables_in_LiPe"]
            i += 1
        self.db.commit()  
        return nesteddict

    def getTable(self, tablename):
        cur = self.db.cursor(dictionary=True)
        sql = "SELECT * FROM " + tablename
        cur.execute(sql)
        cur.close()
        rows = cur.fetchall()
        nesteddict = {}
        for row in rows:
            nesteddict[row["id"]] = row
        self.db.commit()
        return nesteddict

    def getLastXTableRows(self, tablename, x):
        cur = self.db.cursor(dictionary=True)
        sql = "SELECT * FROM " + tablename + " ORDER BY id DESC LIMIT " + str(x)
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        nesteddict = {}
        for row in rows:
            nesteddict[row["id"]] = row
        self.db.commit()
        return nesteddict

    def Test(self):
        result = "<h1>Dies ist ein Test</h1>"
        time.sleep(5)
        return(result)

    def close(self):
        self.db.close()

    






