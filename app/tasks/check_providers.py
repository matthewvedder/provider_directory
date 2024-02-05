from app import celery

@celery.task
def example_task(x, y):
    return x + y