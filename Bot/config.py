import os

bot_token = '814421679:AAGn-xW9ARssv0-7j-pyagCMn5tmrYEk50Y'
owm_token = 'e0a3aa1277572215e68425c76dc67592'

MONGODB_URI = 'mongodb+srv://WeatherBot:vCVaDVvEqRf6zZs@cluster0.xicxe.mongodb.net/WeatherBotDB?retryWrites=true&w=majority'

HEROKU_APP_NAME = 'bagirtelegramweatherbot'

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{bot_token}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT', 5000))