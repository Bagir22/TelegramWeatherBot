from pyowm import OWM
from pyowm.utils.config import get_default_config

import config


config_dict = get_default_config()
config_dict['language'] = 'en'

owm = OWM(config.owm_token, config_dict)
mgr = owm.weather_manager()

'''
print(w.humidity," 12 строчка") # Важно влажность
print(w.pressure," 13 строчка") # Важно давление
print(w.rain," 14 строчка") #
print(w.ref_time," 15 строчка") #
print(w.snow," 16 строчка") #
print(w.srise_time," 17 строчка") #
print(w.sset_time," 18 строчка") # 
print(w.status," 19 строчка") # Важно
print(w.temp," 20 строчка") # Важно
print(w.uvi," 21 строчка") #
print(w.weather_code," 22 строчка") #
'''

def currently_weather(latitude, longitude):

    one_call = mgr.one_call(lat=float(latitude), lon=float(longitude))
    w = one_call.current
    current_detailed = w.detailed_status
    current_humidity = w.humidity
    current_pressure = round(w.pressure['press']/(1.333223684),0)
    current_temp = w.temp

    return current_detailed,current_humidity,current_pressure,current_temp


def today_weather(latitude, longitude):
    one_call = mgr.one_call(lat=float(latitude), lon=float(longitude))
    w = one_call.forecast_daily[0]
    today_detailed = w.detailed_status
    today_humidity = w.humidity
    today_pressure = round(w.pressure['press']/(1.333223684),0)
    today_temp = w.temp

    return today_detailed,today_humidity,today_pressure,today_temp


def tomorrow_weather(latitude, longitude):
    one_call = mgr.one_call(lat=float(latitude), lon=float(longitude))
    w = one_call.forecast_daily[1]
    tomorrow_detailed = w.detailed_status
    tomorrow_humidity = w.humidity
    tomorrow_pressure = round(w.pressure['press']/(1.333223684),0)
    tomorrow_temp = w.temp

    return tomorrow_detailed,tomorrow_humidity,tomorrow_pressure,tomorrow_temp


def week_weather(latitude, longitude):
    one_call = mgr.one_call(lat=float(latitude), lon=float(longitude))
    week = []
    for i in range(0,6):
        w = one_call.forecast_daily[i]
        day = {
                'day_time' : w.reference_time,
                'day_detailed' : w.detailed_status,
                'day_humidity' : w.humidity,
                'day_pressure' : w.pressure,
                'day_status' : w.status,
                'day_temp' : w.temp}
        week.append(day)

    return week
