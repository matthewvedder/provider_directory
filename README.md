pip freeze > requirements.txt
pip install -r requirements.txt

flask run

pytest

source myenv/bin/activate


from app.app import db
from app.models.provider import Provider
db.create_all()

celery -A make_celery worker --loglevel INFO
celery -A make_celery flower





from app.models.provider import Provider
from app.app import db
last_provider = Provider.query.order_by(Provider.id.desc()).first()
last_provider.state = "OH"
db.session.commit()

from app.tasks.check_providers import initiate_provider_updates
initiate_provider_updates()

