FROM python:3.9

COPY /requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r /app/requirements.txt

COPY . /app

CMD ["python3", "/app/Bot/bot.py"; "python3", "/app/Bot/bot.py";]