from app import db

class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    service = db.Column(db.String(128), nullable=False)

    def __init__(self, name, service):
        self.name = name
        self.service = service