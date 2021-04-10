FROM python:3.9

COPY /requirements.txt /bot/requirements.txt

WORKDIR /bot/bot/

RUN pip install -r /bot/requirements.txt

COPY . /bot/bot/

CMD ["python3", "bot.py"]