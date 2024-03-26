FROM python:3.10

RUN mkdir /translator_bot

WORKDIR /translator_bot

RUN pip install aiogram==2.25.1

COPY . /translator_bot/
