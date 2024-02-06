import pytest
from flask_testing import TestCase
from app.app import create_app, db
from app.models.provider_archive import ProviderArchive
from datetime import datetime

provider_data = {
    'original_provider_id': 1,  
    'npi': "1234567890",
    'name': "John Doe",
    'npi_type': "Individual",
    'primary_practice_address': "123 Main St, Anytown, USA",
    'city': "Anytown",
    'state': "NY",
    'postal_code': "12345",
    'phone': "555-555-5555",
    'primary_taxonomy': "General Practice"
}

class TestProviderArchiveModel(TestCase):
    def create_app(self):
        # Import the configuration specific to testing
        app = create_app('test_config.py')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_provider_archive(self):
        # Create a new ProviderArchive instance
        provider_archive = ProviderArchive(**provider_data)

        db.session.add(provider_archive)
        db.session.commit()

        # Retrieve the provider archive from the database
        retrieved_provider_archive = ProviderArchive.query.first()

        # Assertions to ensure the provider archive was correctly added and fields are correct
        assert retrieved_provider_archive.npi == "1234567890"
        assert retrieved_provider_archive.name == "John Doe"
        assert retrieved_provider_archive.npi_type == "Individual"
        assert retrieved_provider_archive.primary_practice_address == "123 Main St, Anytown, USA"
        assert retrieved_provider_archive.phone == "555-555-5555"
        assert retrieved_provider_archive.primary_taxonomy == "General Practice"

    def test_update_provider(self):
        # Create a new ProviderArchive instance
        provider_archive = ProviderArchive(**provider_data)

        db.session.add(provider_archive)
        db.session.commit()

        # Retrieve the provider archive from the database
        retrieved_provider_archive = ProviderArchive.query.first()

        # Update the provider archive's name
        retrieved_provider_archive.name = "Jane Doe"
        db.session.commit()

        # Retrieve the provider archive from the database
        updated_provider_archive = ProviderArchive.query.first()

        # Assertions to ensure the provider archive was correctly updated
        assert updated_provider_archive.name == "Jane Doe"

    def test_delete_provider(self):
        # Create a new ProviderArchive instance
        provider_archive = ProviderArchive(**provider_data)


        db.session.add(provider_archive)
        db.session.commit()

        # Retrieve the provider archive from the database
        retrieved_provider_archive = ProviderArchive.query.first()

        # Delete the provider archive
        db.session.delete(retrieved_provider_archive)
        db.session.commit()

        # Retrieve the provider archive from the database
        deleted_provider_archive = ProviderArchive.query.first()

        # Assertions to ensure the provider archive was correctly deleted
        assert deleted_provider_archive is None