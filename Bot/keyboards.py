from aiogram import types


def main_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard_wth = types.InlineKeyboardButton(text="Weather", callback_data="weather_button")
    keyboard_stn = types.InlineKeyboardButton(text="Settings", callback_data="settings_button")
    keyboard_about = types.InlineKeyboardButton(text="Information", callback_data="about_button")
    keyboard.add(keyboard_wth, keyboard_stn, keyboard_about)
    return keyboard


def weather_keyboard():
    wth_key = types.InlineKeyboardMarkup()
    btn_weather_now = types.InlineKeyboardButton(text="Weather now", callback_data="weather_currently_button")
    btn_weather_today = types.InlineKeyboardButton(text="Weather today", callback_data="weather_today_button")
    btn_weather_tomorrow = types.InlineKeyboardButton(text="Weather tomorrow ", callback_data="weather_tomorrow_button")
    btn_weather_week = types.InlineKeyboardButton(text="Weather week ", callback_data="weather_week_button")
    back_button = types.InlineKeyboardButton(text="Back", callback_data="back_button")
    wth_key.row(btn_weather_now)
    wth_key.row(btn_weather_today)
    wth_key.row(btn_weather_tomorrow)
    wth_key.row(btn_weather_week)
    wth_key.row(back_button)
    return wth_key


def settings_keyboard():
    stn_key = types.InlineKeyboardMarkup()
    btn_location_set = types.InlineKeyboardButton(text="Location", callback_data="set_location_button")
    btn_timer_set = types.InlineKeyboardButton(text="Timer", callback_data="set_timer_button")
    back_button = types.InlineKeyboardButton(text="Back", callback_data="back_button")
    stn_key.add(btn_location_set, btn_timer_set)
    stn_key.row(back_button)
    return stn_key


def about_keyboard():
    about_key = types.InlineKeyboardMarkup()
    btn_about = types.InlineKeyboardButton(text="About Bot", callback_data="about button")
    back_button = types.InlineKeyboardButton(text="Back", callback_data="back_button")
    about_key.add(btn_about)
    about_key.row(back_button)
    return about_key


def timer_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard_onTimer = types.InlineKeyboardButton(text="Timer On", callback_data="onTimer")
    keyboard_OffTimer = types.InlineKeyboardButton(text="Timer Off", callback_data="offTimer")
    keyboard.add(keyboard_onTimer, keyboard_OffTimer)
    return keyboard