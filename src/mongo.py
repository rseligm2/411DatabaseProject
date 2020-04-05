import subprocess

import pymongo

subprocess.Popen(["mongod", "--dbpath", "./data/mongodb"])
client = pymongo.MongoClient()
database = client.football

users = database.users
# word_cloud = database.
