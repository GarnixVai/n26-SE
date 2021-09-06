import mysql.connector as mysql
from flask import Flask, request, render_template, render_template_string, jsonify
from library.mock_data import MockData
import json

class Database():
    def __init__(self, host = "localhost", user = "root", pwd = "1234"):
        self.db = mysql.connect(
            host = host,
            user = user,
            passwd = pwd)
        self.mockData = MockData()
        self.cursor = self.db.cursor()
        self.initDatabase()
    
    def initDatabase(self):
        self.createDatabase()
        self.createTable()
        # cursor = self.db.cursor()
        result = self.cursor.execute("SELECT count(*) FROM configuration")
        rows_count = self.cursor.fetchone()[0]
        # if the table is empty, generate mock data
        if rows_count == 0:
            self.setDatabase()

    def readJson(self, filename):
        o = json.loads(open(filename, "r").read())
        return o

    def createDatabase(self):
        sql = "CREATE DATABASE IF NOT EXISTS MCC;"
        self.cursor.execute(sql)
        self.cursor.execute("USE MCC;")
        self.db.commit()

    def createTable(self):
        # create table
        sqlConfig = '''create table IF NOT EXISTS configuration (id int NOT NULL AUTO_INCREMENT,
                jsonData  text NOT NULL,
                PRIMARY KEY (id));
            '''
        self.cursor.execute(sqlConfig)

        sqlDelta = '''create table IF NOT EXISTS delta (id int NOT NULL AUTO_INCREMENT,
            jsonData  text NOT NULL,
            PRIMARY KEY (id));
            '''
        self.cursor.execute(sqlDelta)
        self.db.commit()

    def insertConfigTableWithId(self, id, jsondata):
        secursor = self.db.cursor()
        sql = "insert into configuration (id, jsonData) values(" + str(id)+ ",'"+  jsondata+"')"
        cursor.execute(sql)
        cursor.close()

    def insertConfigTable(self, jsondata, dbcommit):
        cursor = self.db.cursor()
        # sql = "insert into configuration (id, jsonData) values(" + str(id)+ ",'"+  jsondata+"')"
        sql = "insert into configuration (jsonData) values('"+  jsondata+"')"
        # print("sql:", sql)
        cursor.execute(sql)
        if dbcommit:
           self.db.commit()
        cursor.close()

    def updateConfigTable(self, id, jsondata):
        cursor = self.db.cursor()
        sql = "UPDATE configuration SET jsonData = '" +  jsondata+"' where id=" +  str(id)
        cursor.execute(sql)
        self.db.commit()
        cursor.close()
        

    def insertDeltaTable(self, jsondata, dbcommit):
        cursor = self.db.cursor()
        sql = "insert into delta (jsonData) values(" + "'"+  jsondata+"')"
        cursor.execute(sql)
        if dbcommit:
            self.db.commit()
        cursor.close()

    def selectAllConfig(self):
        cursor = self.db.cursor()
        sql = "select * from configuration;"
        cursor.nextset()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close() 
        configList = []
        for r in result:
            (id, data) = r
            d = json.loads(data)
            d["id"] = str(id)
            # print(type(d), d, type(id),  id)
            configList.append(d)
        return configList


    def selectAllDelta(self):
        cursor = self.db.cursor()
        sql = "select * from delta;"
        cursor.nextset()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close() 
        deltaList = []
        for r in result:
            (id, data) = r
            d = json.loads(data)
            d["id"] = str(id)
            deltaList.append(d)
        return deltaList

    # disconnect from server
    def closeDatabase(self):
        self.db.close()

    def setDatabase(self):
        for i in range(15):
            print(i)
            id = i + 1
            (config, app, owner, roles) = self.mockData.generateConfig(id)
            delta = self.mockData.generateDelta(id, app, owner, roles)
            self.insertConfigTable(config, False)
            self.insertDeltaTable(delta, False)
        self.db.commit()

