from .celery import app
from models.news.JawaPos import JawaPos, JawaPosNasional, JawaPosFinance, JawaPosBisnis
from time import sleep


@app.task()
def task1():
    sleep(10)


@app.task()
def task2():
    sleep(20)


@app.task()
def task3():
    sleep(30)


@app.task()
def task4():
    sleep(35)
