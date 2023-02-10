import os
import pymongo
import json


MONGO_USER = os.getenv("MONGO_USER", "admin")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "P4ssW0rD")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")


def get_mongo_uri():
    return f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"


def init_db():
    myclient = pymongo.MongoClient(get_mongo_uri())
    mydb = myclient["schedule"]

    # load data
    with open("init_data.json") as f:
        init_data = json.load(f)
    
    # insert classes
    if "classroom" not in mydb.list_collection_names():
        mycol = mydb["classroom"]
        mycol.insert_many(init_data["classroom"])

    # close
    myclient.close()


if __name__ == "__main__":
    init_db()
