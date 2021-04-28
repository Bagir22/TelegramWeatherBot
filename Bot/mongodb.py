from pymongo import MongoClient
from config import MONGODB_URI


cluster = MongoClient(MONGODB_URI)

db = cluster["WeatherBotDB"]
collection = db["WeatherBotCollection"]


def insert_data_into_db(id, latitude=None, longitude=None, timerState=None, hours=None, minutes=None):
    collection.update({"_id": id}, {"$set": {"latitude": latitude, "longitude": longitude, "timerState": timerState, "hours": hours, "minutes":minutes}}, upsert=True)


def update_location(id, latitude, longitude):
    collection.update_one(
        {"_id": id}, {"$set": {"latitude": latitude, "longitude": longitude}})


def update_timerState(id, timerState):
    collection.update_one(
        {"_id": id}, {"$set": {"timerState": timerState}})


def update_time(id, hours, minutes):
    collection.update_one(
        {"_id": id}, {"$set": {"hours": hours, "minutes":minutes}})


def get_location_from_db(id):
    latitude = collection.find_one({"_id": id})["latitude"]
    longitude = collection.find_one({"_id": id})["longitude"]

    return latitude, longitude


def get_timerState_from_db(id):
    timerState = collection.find_one({"_id": id})["timerState"]

    return timerState


def get_time_from_db(id):
    hours = collection.find_one({"_id": id})["hours"]
    minutes = collection.find_one({"_id": id})["minutes"]

    return minutes
