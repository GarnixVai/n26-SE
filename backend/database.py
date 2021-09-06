import mysql.connector as mysql
from flask import Flask, request, render_template, render_template_string, jsonify
from operation import generateConfig, generateDelta
import json
db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "1234"
)
## creating an instance of 'cursor' class which is used to execute the 'SQL' statements in 'Python'
cursor = db.cursor()
def initDatabase():
    # generateJsonFile()
    createDatabase()
    createTable()
def readJson(filename):
    o = json.loads(open(filename, "r").read())
    return o

def createDatabase():
    sql = "CREATE DATABASE IF NOT EXISTS MCC;"
    cursor.execute(sql)
    cursor.execute("USE MCC;")
    db.commit()

def createTable():
    # create table
    sqlConfig = '''create table IF NOT EXISTS configuration (id int NOT NULL AUTO_INCREMENT,
            jsonData  text NOT NULL,
            PRIMARY KEY (id));
           '''
    cursor.execute(sqlConfig)

    sqlDelta = '''create table IF NOT EXISTS delta (id int NOT NULL AUTO_INCREMENT,
        jsonData  text NOT NULL,
        PRIMARY KEY (id));
        '''
    cursor.execute(sqlDelta)

    db.commit()

def insertConfigTableWithId(id, jsondata):
    cursor = db.cursor()
    sql = "insert into configuration (id, jsonData) values(" + str(id)+ ",'"+  jsondata+"')"
    # print("sql:", sql)
    cursor.execute(sql)
    db.commit()
    cursor.close()

def insertConfigTable(jsondata):
    cursor = db.cursor()
    # sql = "insert into configuration (id, jsonData) values(" + str(id)+ ",'"+  jsondata+"')"
    sql = "insert into configuration (jsonData) values('"+  jsondata+"')"
    # print("sql:", sql)
    cursor.execute(sql)
    db.commit()
    cursor.close()

def updateConfigTable(id, jsondata):
    cursor = db.cursor()
    sql = "UPDATE configuration SET jsonData = '" +  jsondata+"' where id=" +  str(id)
    # print("sql:", sql)
    cursor.execute(sql)
    db.commit()
    cursor.close()
    

def insertDeltaTable(jsondata):
    cursor = db.cursor()
    sql = "insert into delta (jsonData) values(" + "'"+  jsondata+"')"
    # print("sql:", sql)
    cursor.execute(sql)
    db.commit()
    cursor.close()

def selectAllConfig():
    cursor = db.cursor()
    sql = "select * from configuration;"
    cursor.nextset()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close() 
    configList = []
    for r in result:
        (id, data) = r
        d = json.loads(data)
        # print(type(d), d, type(id),  id)
        d["id"] = str(id)
        # print(type(d), d, type(id),  id)
        configList.append(d)
    return configList


def selectAllDelta():
    cursor = db.cursor()
    sql = "select * from delta;"
    cursor.nextset()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close() 
    deltaList = []
    for r in result:
        (id, config_id, data) = r
        d = json.loads(data)
        d["id"] = str(id)
        deltaList.append(d)
    return deltaList

# disconnect from server
def closeDatabase():
    db.close()

def setDatabase():
    for i in range(15):
        print(i)
        id = i + 2
        (config, app, owner, roles) = generateConfig(i)
        delta = generateDelta(id, app, owner, roles)
        insertConfigTableWithId(id, config)
        insertDeltaTable(id, delta)
    db.commit()

def initDataset():
    # (config, app, owner, roles) = generateConfig(1)
    # insertConfigTable(1, config)
    pass
if __name__ == '__main__':
    initDatabase()
    # setDatabase()
    # selectAllConfig()
    # delta = generateDelta(1, "almost.jpg", "Robert Holmes", [{"name": "test", "permission": ["Delete"]}])
    # insertDeltaTable(1, delta)
    # selectAllDelta()


