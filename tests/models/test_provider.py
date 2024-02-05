import pytest
from flask_testing import TestCase
from app.app import create_app, db
from app.models.provider import Provider

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