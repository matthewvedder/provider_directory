pip freeze > requirements.txt
pip install -r requirements.txt

flask run

pytest

source venv/bin/activate

from app.app import db
from app.models.provider import Provider
db.create_all()

celery -A make_celery worker --loglevel INFO
celery -A make_celery flower


from app.tasks.check_providers import initiate_provider_updates
initiate_provider_updates()

