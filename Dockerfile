FROM python:3.9

COPY /requirements.txt /bot/requirements.txt

WORKDIR /app

RUN pip install -r /requirements.txt

COPY . /app

CMD ["python3", "/app/Bot/bot.py"]