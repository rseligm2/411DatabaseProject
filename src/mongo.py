import subprocess

import pymongo

from pymongo import collection, database


subprocess.Popen(["mongod", "--dbpath", "./data/mongodb"])
client = pymongo.MongoClient()
football_db: database.Database = client.football

users_col: collection.Collection = football_db.users
comments_col: collection.Collection = football_db.comments
team_comments_col: collection.Collection = football_db.team_comments

# word_cloud = database.
