FROM python:3.9.4-slim

MAINTAINER Chaeyong Chong "cychong@gmail.com"

RUN mkdir /app
WORKDIR /app

ADD requirements.txt app.py telegram_send.py /app/

RUN python -m pip install --upgrade pip && \
	pip install --no-cache-dir -r requirements.txt

CMD ["python3", "-u", "app.py"]
