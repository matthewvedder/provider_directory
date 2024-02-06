from app.app import db
from datetime import datetime

class ProviderArchive(db.Model):
    __tablename__ = 'providers_archive'

    id = db.Column(db.Integer, primary_key=True)
    original_provider_id = db.Column(db.Integer, db.ForeignKey('providers.id'), nullable=False)
    npi = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(255), nullable=True, default=None)
    npi_type = db.Column(db.String(50), nullable=True, default=None)
    primary_practice_address = db.Column(db.String(255), nullable=True, default=None)
    city = db.Column(db.String(100), nullable=True, default=None) 
    state = db.Column(db.String(2), nullable=True, default=None) 
    postal_code = db.Column(db.String(10), nullable=True, default=None) 
    phone = db.Column(db.String(20), nullable=True, default=None)
    primary_taxonomy = db.Column(db.String(255), nullable=True, default=None)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    archived_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, original_provider_id, npi, name=None, npi_type=None, primary_practice_address=None, city=None, state=None, postal_code=None, phone=None, primary_taxonomy=None):
        self.original_provider_id = original_provider_id
        self.npi = npi
        self.name = name
        self.npi_type = npi_type
        self.primary_practice_address = primary_practice_address
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.phone = phone
        self.primary_taxonomy = primary_taxonomy

    def __repr__(self):
        return f'<ProviderArchive {self.name if self.name else "Unnamed"} NPI: {self.npi}>'