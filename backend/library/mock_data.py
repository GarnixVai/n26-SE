from faker import Faker
from random import randrange, random
import json
import datetime as dt

class MockData():
    def __init__(self):
        Faker.seed(0)
        self.fake = Faker()

    # generate config
    def generateConfig(self, id):
        latestChange = self.fake.date_between(start_date='-2y', end_date='today')
        latestChange = latestChange.strftime('%d-%m-%Y %H:%M:%S')
        print(latestChange)
        name = self.fake.file_name(extension=None)
        owner = self.fake.name()
        roles = []
        for _ in range(5):
            n = self.fake.name()
            roles.append({"name": n, "permission": ["Create", "Edit"]})
        metaData = {
            "configManager": owner,
            "name": name,
            "owner": owner
        }
        config = {
            "id": id,
            "latestChange": latestChange,
            "name": name,
            "owner": owner,
            "metaData": metaData, 
            "techData": {
                "roles": roles
            }
        }
        return (json.dumps(config), name, owner, roles)

    # generate delta
    def generateDelta(self, id, app, owner, roles):
        editor = self.fake.name()
        timestamp = self.fake.date_between(start_date='-1y', end_date='today')
        timestamp = timestamp.strftime('%d-%m-%Y %H:%M:%S')
        delta = {
            "config_id": id,
            "editor": editor,
            "message": "initialize delta",
            "timestamp": timestamp,
            "change":{
                "techData":{
                    "roles": roles
                },
                "metaData":{
                    "configManager": editor,
                    "name": app,
                    "owner": owner
                }
            }

        }
        return json.dumps(delta)

    # For comparing test: generate config file
    def generateJsonFile(self):
        configurationList = []
        deltaList = []
        config_file = open("data/config.json", "w")
        delta_file = open("data/delta.json", "w")
        for i in range(15):
            id = i + 1
            (config, app, owner, roles) = generateConfig(i)
            delta = generateDelta(id, app, owner, roles)
            configurationList.append(config)
            deltaList.append(delta)
        json.dump(json.dumps(configurationList), config_file)
        json.dump(json.dumps(deltaList), delta_file)
    