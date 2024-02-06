import pytest
from flask_testing import TestCase
from app.app import create_app, db
from app.models.provider import Provider
from app.models.provider_archive import ProviderArchive
from datetime import datetime

class TestProviderModel(TestCase):
    def create_app(self):
        # Import the configuration specific to testing
        app = create_app('test_config.py')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_provider(self):
        # Create a new Provider instance
        provider = Provider(
            npi="1234567890",
            name="John Doe",
            npi_type="Individual",
            primary_practice_address="123 Main St, Anytown, USA",
            phone="555-555-5555",
            primary_taxonomy="General Practice"
        )

        db.session.add(provider)
        db.session.commit()

        # Retrieve the provider from the database
        retrieved_provider = Provider.query.first()

        # Assertions to ensure the provider was correctly added and fields are correct
        assert retrieved_provider.npi == "1234567890"
        assert retrieved_provider.name == "John Doe"
        assert retrieved_provider.npi_type == "Individual"
        assert retrieved_provider.primary_practice_address == "123 Main St, Anytown, USA"
        assert retrieved_provider.phone == "555-555-5555"
        assert retrieved_provider.primary_taxonomy == "General Practice"

    def test_update_provider(self):
        # Create a new Provider instance
        provider = Provider(
            npi="1234567890",
            name="John Doe",
            npi_type="Individual",
            primary_practice_address="123 Main St, Anytown, USA",
            phone="555-555-5555",
            primary_taxonomy="General Practice"
        )

        db.session.add(provider)
        db.session.commit()

        # Retrieve the provider from the database
        retrieved_provider = Provider.query.first()

        # Update the provider's name
        retrieved_provider.name = "Jane Doe"
        db.session.commit()

        # Retrieve the provider from the database
        updated_provider = Provider.query.first()

        # Assertions to ensure the provider was correctly updated
        assert updated_provider.name == "Jane Doe"
    
    def test_delete_provider(self):
        # Create a new Provider instance
        provider = Provider(
            npi="1234567890",
            name="John Doe",
            npi_type="Individual",
            primary_practice_address="123 Main St, Anytown, USA",
            phone="555-555-5555",
            primary_taxonomy="General Practice"
        )

        db.session.add(provider)
        db.session.commit()

        # Retrieve the provider from the database
        retrieved_provider = Provider.query.first()

        # Delete the provider
        db.session.delete(retrieved_provider)
        db.session.commit()

        # Retrieve the provider from the database
        deleted_provider = Provider.query.first()

        # Assertions to ensure the provider was correctly deleted
        assert deleted_provider is None
    
    def test_provider_repr(self):
        # Create a new Provider instance
        provider = Provider(
            npi="1234567890",
            name="John Doe",
            npi_type="Individual",
            primary_practice_address="123 Main St, Anytown, USA",
            phone="555-555-5555",
            primary_taxonomy="General Practice"
        )

        # Assertions to ensure the __repr__ method returns the expected string
        assert str(provider) == "<Provider John Doe NPI: 1234567890>"

    def test_create_provider_only_npi(self):
        # Create a new Provider instance with only the NPI field
        provider = Provider(
            npi="1234567890"
        )

        db.session.add(provider)
        db.session.commit()

        # Retrieve the provider from the database
        retrieved_provider = Provider.query.first()
        assert retrieved_provider.npi == "1234567890"
    
    def test_archive_provider(self):
        # Create a new Provider instance
        provider = Provider(
            npi="1234567890",
            name="Test Provider",
            npi_type="Individual",
            primary_practice_address="123 Main St, Anytown, USA",
            phone="555-555-5555",
            primary_taxonomy="General Practice"
        )
        db.session.add(provider)
        db.session.commit()

        # Archive the provider
        provider.archive()

        # Fetch the archived provider
        archived_provider = ProviderArchive.query.filter_by(original_provider_id=provider.id).first()

        # Assertions
        assert archived_provider is not None
        assert archived_provider.npi == provider.npi
        assert archived_provider.name == provider.name
        assert archived_provider.npi_type == provider.npi_type
        # Add more assertions as necessary to cover all fields
        
        # Optionally, check the timestamp is reasonable (e.g., not in the future)
        assert archived_provider.archived_at <= datetime.utcnow()