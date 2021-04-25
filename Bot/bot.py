from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.executor import start_webhook

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import re

import config

import keyboards
import owm
import mongodb


bot = Bot(token=config.bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


scheduler = AsyncIOScheduler()


class BotStartState(StatesGroup):
    cityState = State()
    timerState = State()
    setTimer = State()


async def on_startup(dp):
    await bot.set_webhook(config.WEBHOOK_URL, drop_pending_updates=True)


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('ОК')


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message, state: FSMContext):
    await BotStartState.cityState.set()
    mongodb.insert_data_into_db(id=message.chat.id)
    await message.answer('Hello, I am the Bot that can send you weather' +
                         '\nLet' + 's move on to configuring' +
                         '\nTo do this, send me your geolocation')


@dp.message_handler(content_types="location", state=BotStartState.cityState)
async def process_location_set(message: types.Message, state: FSMContext):
    #global latitude, longitude
    latitude = message.location.latitude
    longitude = message.location.longitude
    id = message.chat.id
    mongodb.update_location(id, latitude, longitude)
    await message.answer("Ok, now turn the timer on or off", reply_markup=keyboards.timer_keyboard())
    await BotStartState.next()


@dp.callback_query_handler(text='onTimer', state=BotStartState.timerState)
async def process_timerOnState_set(call: types.CallbackQuery, state: FSMContext):
    text = "The timer is on, now send me the timer time in the format xx:xx"
    id = call.message.chat.id
    timerState = True

    mongodb.update_timerState(id, timerState)
    await call.message.answer(text)
    await BotStartState.next()


@dp.callback_query_handler(text='offTimer', state=BotStartState.timerState)
async def process_timerOffState_set(call: types.CallbackQuery, state: FSMContext):
    text = "The timer is off \nGood, the bot is running"
    id = call.message.chat.id
    timerState = False

    mongodb.update_timerState(id, timerState)

    await call.message.answer(text, reply_markup=keyboards.main_keyboard())
    await BotStartState.next()
    await BotStartState.next()


@dp.message_handler(state=BotStartState.setTimer)
async def process_timer_set(message: types.message, state: FSMContext):
    id = message.chat.id
    timer_message = message.text
    if re.match(r'\w\w:\w\w', timer_message):
        result = re.split(r':', timer_message)
        if 13 < int(result[0]) < 20:
            if re.match(r'[1][4-9]', result[0]) and re.match(r'[0-5]\d', result[1]):
                time1 = result[0]
                time2 = result[1]
                chat_id = message.chat.id
                await schedule_jobs(time1, time2, chat_id)

                await message.answer("Good, the bot is running", reply_markup=keyboards.main_keyboard())
                mongodb.update_time(id, timer_message)
                await state.finish()
            else:
                await message.answer("Hmmm, the format of the entered data is wrong!" +
                                      "\nTry again!")
        else:
            if re.match(r'[0-2][0-3]', result[0]) and re.match(r'[0-5]\d', result[1]):
                time1 = result[0]
                time2 = result[1]
                chat_id = message.chat.id
                await schedule_jobs(time1, time2, chat_id)
                mongodb.update_time(id, timer_message)
                await message.answer("Good, the bot is running", reply_markup=keyboards.main_keyboard())
                await state.finish()
            else:
                await message.answer("Hmmm, the format of the entered data is wrong!" +
                                      "\nTry again!")
    else:
        await message.answer("Hmmm, the format of the entered data is wrong!" +
                                      "\nTry again!")


@dp.callback_query_handler(text='weather_currently_button')
async def send_currently_weather(call: types.CallbackQuery):
    latitude, longitude = mongodb.get_location_from_db(call.message.chat.id)
    current_detailed, current_humidity, current_pressure, current_temp = owm.currently_weather(latitude, longitude)
    await call.message.answer(f"Now - {current_detailed}" +
                              f"\nHumidity - {current_humidity} %" +
                              f"\nPressure - {str(current_pressure)} mmHg" +
                              f"\nTemperature now - {str('%.0f' % round(current_temp['temp'] - 273))}" +
                              f"\nFeels like - {str('%.0f' % round(current_temp['feels_like'] - 273))}",
                              reply_markup=keyboards.weather_keyboard())


@dp.callback_query_handler(text='weather_today_button')
async def send_today_weather(call: types.CallbackQuery):
    latitude, longitude = mongodb.get_location_from_db(call.message.chat.id)
    today_detailed, today_humidity, today_pressure, today_temp = owm.today_weather(latitude, longitude)
    await call.message.answer(f"Now - {today_detailed}" +
                              f"\nHumidity - {today_humidity} %" +
                              f"\nPressure - {str(today_pressure)} mmHg" +
                              f"\nTemperature - {str('%.0f' % round(today_temp['day'] - 273))}" +
                              f"\nFeels like - {str('%.0f' % round(today_temp['feels_like_day'] - 273))}",
                              reply_markup=keyboards.weather_keyboard())


async def send_automatically_today_weather(message: types.Message, chat_id):
    latitude, longitude = mongodb.get_location_from_db(chat_id)
    today_detailed, today_humidity, today_pressure, today_temp = owm.today_weather(latitude, longitude)
    await bot.send_message(chat_id=chat_id, text=(f"Now - {today_detailed}" +
                                                  f"\nHumidity - {today_humidity} %" +
                                                  f"\nPressure - {str(today_pressure)} mmHg" +
                                                  f"\nTemperature - {str('%.0f' % round(today_temp['day'] - 273))}" +
                                                  f"\nFeels like - {str('%.0f' % round(today_temp['feels_like_day'] - 273))}"),
                           reply_markup=keyboards.weather_keyboard())


@dp.callback_query_handler(text='weather_tomorrow_button')
async def send_tomorrow_weather(call: types.CallbackQuery):
    latitude, longitude = mongodb.get_location_from_db(call.message.chat.id)
    tomorrow_detailed, tomorrow_humidity, tomorrow_pressure, tomorrow_temp = owm.tomorrow_weather(latitude, longitude)
    await call.message.answer(f"Tomorrow - {tomorrow_detailed}"
                              f"\nHumidity - {tomorrow_humidity} %"
                              f"\nPressure - {str(tomorrow_pressure)} mmHg"
                              f"\nTemperature - {str('%.0f' % round(tomorrow_temp['day'] - 273))}"
                              f"\nFeels like - {str('%.0f' % round(tomorrow_temp['feels_like_day'] - 273))}",
                              reply_markup=keyboards.weather_keyboard())


@dp.callback_query_handler(text='weather_week_button')
async def send_week_weather(call: types.CallbackQuery):
    latitude, longitude = mongodb.get_location_from_db(call.message.chat.id)
    week = owm.week_weather(latitude, longitude)
    week_text = ""
    weekdays = ['Sunday',
                'Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday']
    for i in range(0, 6):
        t = f"\nAt {weekdays[i]} {week[i]['day_detailed']} \nTemperature - {('%.0f' % round(week[i]['day_temp']['day'] - 273))} degrees Celsius"
        week_text += t
    await call.message.answer(week_text, reply_markup=keyboards.weather_keyboard())


async def schedule_jobs(time1, time2, chat_id):
    scheduler.add_job(send_automatically_today_weather, 'cron', day_of_week='mon-sun', hour=time1, minute=time2,
                      args=(dp, chat_id))


@dp.callback_query_handler(text='set_location_button')
async def process_change_location(call: types.CallbackQuery):
    await call.message.answer("Please share your geolocation to update your location")


@dp.message_handler(content_types="location")
async def process_get_change_location(message: types.Message):
    #global latitude, longitude
    latitude = message.location.latitude
    longitude = message.location.longitude

    id = message.chat.id
    mongodb.update_location(id, latitude, longitude)

    await message.answer("Ok, new geolocation received", reply_markup=keyboards.settings_keyboard())


@dp.callback_query_handler(text='set_timer_button')
async def process_change_timer(call: types.CallbackQuery, state:FSMContext):
    await BotStartState.timerState.set()
    await call.message.answer("Please turn on or off the timer"
                              , reply_markup=keyboards.timer_keyboard())


'''
@dp.message_handler()
async def process_get_change_timer(message: types.message):
    await message.answer("Please turn on or off the timer", reply_markup=keyboards.timer_keyboard())
'''


@dp.callback_query_handler(text='weather_button')
async def set_weather_keyboard(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=keyboards.weather_keyboard())

@dp.message_handler(commands=['settings'])
@dp.callback_query_handler(text='settings_button')
async def set_settings_keyboard(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=keyboards.settings_keyboard())


@dp.callback_query_handler(text='about_button')
async def set_about_keyboard(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=keyboards.about_keyboard())


@dp.callback_query_handler(text='back_button')
async def set_main_keyboard_back_button(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=keyboards.main_keyboard())



if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=config.WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=config.WEBAPP_HOST,
        port=config.WEBAPP_PORT
    )

    scheduler.start()