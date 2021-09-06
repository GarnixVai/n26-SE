from flask import Flask, request, make_response, jsonify, abort
from flask_cors import CORS, cross_origin
import os, sys, threading, json, time
from library.init import create_app
from library.mysql_db import Database 
sys.path.append(".")

app = create_app()
manual = input("Manually input  mysql criteria(y/n)?")
DB = None
if(manual.strip().lower() == "y"):
    # Comment out the manual input, use default 
    host = input ("Enter (Mysql)Host :").strip()
    user = input("Enter (Mysql)Root:").strip()
    pwd = input("Enter (Mysql)Password:").strip()
    DB = Database(host = host, user = user, pwd = pwd)
else:
    DB = Database()

# API for getting all configurations
@app.route('/api/v1/configurationList',  methods=['GET'])
@cross_origin()
def get_configurationList():
    # o = json.loads(open("./data/mockConfigData.json", "r").read())
    # return jsonify(o)
    result = DB.selectAllConfig()
    app_json = json.dumps(result)
    o = json.loads(app_json)
    return jsonify(o)

# # API for getting all delta
@app.route('/api/v1/deltaList',  methods=['GET'])
@cross_origin()
def get_deltaList():
    # o = json.loads(open("./data/mockDeltaData.json", "r").read())
    # return jsonify(o)
    result = DB.selectAllDelta()
    app_json = json.dumps(result)
    o = json.loads(app_json)
    return jsonify(o)

# insert new delta(change)
@app.route('/api/v1/delta',  methods=['POST'])
@cross_origin()
def insert_delta():
    if not request.json:
        abort(400)
    delta = request.json
    stringJson = json.dumps(delta)
    try:
        DB.insertDeltaTable(stringJson, True)
        return make_response(jsonify({'success': 'data saved'}), 200) 
    except Exception as err :
        return make_response(jsonify({'error': 'data not saved'}), 500) 


# update configuration
@app.route('/api/v1/configuration/<int:id>',  methods=['POST'])
@cross_origin()
def update_conifg(id):
    if not request.json:
        abort(400)
    config = request.json
    stringJson = json.dumps(config)
    try:
        DB.updateConfigTable(id, stringJson)
        return make_response(jsonify({'success': 'data saved'}), 200) 
    except Exception as err :
        return make_response(jsonify({'error': 'data not saved'}), 500) 

# insert new configuration
@app.route('/api/v1/configurations',  methods=['POST'])
@cross_origin()
def insert_config():
    if not request.json:
        abort(400)
    config = request.json
    stringJson = json.dumps(config)
    try:
        DB.insertConfigTable(stringJson, True)
        return make_response(jsonify({'success': 'data saved'}), 200) 
    except Exception as err :
        return make_response(jsonify({'error': 'data not saved'}), 500) 


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True, reloader=True)
