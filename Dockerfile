FROM python:3.9

COPY /requirements.txt /bot/requirements.txt

WORKDIR /bot

RUN pip install -r /bot/requirements.txt

COPY . /bot

CMD ["python3", "bot.py"]