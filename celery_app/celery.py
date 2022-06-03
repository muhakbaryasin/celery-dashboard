from celery import Celery


app = Celery('celery_app', broker='redis://localhost:6379/4', backend='redis://localhost:6379/4',
             include=['celery_app.tasks'],
             loglevel='INFO',
             task_track_started = True,
             traceback=True)

app.conf.update(result_expires=3600,)

if __name__ == "__main__":
    app.start()
