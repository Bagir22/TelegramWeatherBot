from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot import dp, send_automatically_today_weather


sched = AsyncIOScheduler()

async def schedule_jobs(hours, minutes, id):
    sched.add_job(send_automatically_today_weather, 'cron', day_of_week='mon-sun', hour=hours, minute=minutes,
                      args=(dp, id))


sched.start()

while __name__ == '__main__':
  pass