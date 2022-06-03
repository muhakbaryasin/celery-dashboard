from .celery import app
from models.news.JawaPos import JawaPos, JawaPosNasional, JawaPosFinance, JawaPosBisnis


@app.task()
def task1():
    JawaPos().next()


@app.task()
def task2():
    JawaPosNasional().next()


@app.task()
def task3():
    JawaPosFinance().next()


@app.task()
def task4():
    JawaPosBisnis().next()
