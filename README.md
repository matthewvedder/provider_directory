pip freeze > requirements.txt
flask run

from app.app import db
from app.models.provider import Provider
db.create_all()