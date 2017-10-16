from celery import Celery

app = Celery('tasks', backend='rpc://', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    chain = newsapi.s() | crawl.map() | notifications.s()

@app.task
def newsapi():
    # get articles
    # put in crawl queue
    # put in notifications queue

@app.task
def crawl(article):
    # get crawl lock
    # crawl
    # store results
