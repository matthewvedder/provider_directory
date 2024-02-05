from app.app import celery

@celery.task
def check_providers(x, y):
    return x + y