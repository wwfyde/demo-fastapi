from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//', backend="redis://localhost:6379/0")


@app.task
def add(x, y):
    return x + y
