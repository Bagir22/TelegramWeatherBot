from pymongo import MongoClient

cluster = MongoClient(
    "mongodb+srv://WeatherBot:vCVaDVvEqRf6zZs@cluster0.xicxe.mongodb.net/WeatherBotDB?retryWrites=true&w=majority")
db = cluster["WeatherBotDB"]
collection = db["WeatherBotCollection"]


def insert_data_into_db(id, latitude=None, longitude=None, timerState=None, time=None):
    collection.insert_one(
        {"_id": id, "latitude": latitude, "longitude": longitude, "timerState": timerState, "time": time})


def update_location(id, latitude, longitude):
    collection.insert_one(
        {"_id": id}, {"$set": {"latitude": latitude, "longitude": longitude}})


def update_timerState(id, timerState):
    collection.insert_one(
        {"_id": id}, {"$set": {"timerState": timerState}})


def update_time(id, time):
    collection.insert_one(
        {"_id": id}, {"$set": {"time": time}})


def get_data_from_db(id):
    collection.find_one({"_id": id})
