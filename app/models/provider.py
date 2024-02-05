from app.app import db
from datetime import datetime

class Provider(db.Model):
    __tablename__ = 'providers'

    id = db.Column(db.Integer, primary_key=True)
    npi = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    npi_type = db.Column(db.String(50), nullable=False)
    primary_practice_address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    primary_taxonomy = db.Column(db.String(255), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, npi, name, npi_type, primary_practice_address, phone, primary_taxonomy):
        self.npi = npi
        self.name = name
        self.npi_type = npi_type
        self.primary_practice_address = primary_practice_address
        self.phone = phone
        self.primary_taxonomy = primary_taxonomy

    def __repr__(self):
        return f'<Provider {self.name} NPI: {self.npi}>'