from pymongo import MongoClient
from config import mongodb_password


cluster = MongoClient(
    f"mongodb+srv://WeatherBot:{mongodb_password}@cluster0.xicxe.mongodb.net/WeatherBotDB?retryWrites=true&w=majority")

db = cluster["WeatherBotDB"]
collection = db["WeatherBotCollection"]


def insert_data_into_db(id, latitude=None, longitude=None, timerState=None, time=None):
    collection.update({"_id": id}, {"$set": {"latitude": latitude, "longitude": longitude, "timerState": timerState, "time": time}}, upsert=True)


def update_location(id, latitude, longitude):
    collection.update_one(
        {"_id": id}, {"$set": {"latitude": latitude, "longitude": longitude}})


def update_timerState(id, timerState):
    collection.update_one(
        {"_id": id}, {"$set": {"timerState": timerState}})


def update_time(id, time):
    collection.update_one(
        {"_id": id}, {"$set": {"time": time}})


def get_location_from_db(id):
    latitude = collection.find_one({"_id": id})["latitude"]
    longitude = collection.find_one({"_id": id})["longitude"]

    return latitude, longitude


def get_timerState_from_db(id):
    timerState = collection.find_one({"_id": id})["timerState"]

    return timerState


def get_time_from_db(id):
    time = collection.find_one({"_id": id})["time"]

    return time
