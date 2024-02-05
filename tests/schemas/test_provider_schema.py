from flask_testing import TestCase
from app.app import create_app, db
from app.models.provider import Provider
from app.schemas.provider_schema import ProviderSchema

class TestProviderSchema(TestCase):
    def create_app(self):
        # Import the configuration specific to testing
        return create_app('test_config.py')

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_provider_schema_serialization(self):
        # Create a provider instance
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

        # Serialize the provider instance
        provider_schema = ProviderSchema()
        result = provider_schema.dump(provider)
        self.assertEqual(result['npi'], "1234567890")
        self.assertEqual(result['name'], "John Doe")

    def test_provider_schema_deserialization(self):
        # Prepare a provider dict
        provider_data = {
            "npi": "0987654321",
            "name": "Jane Doe",
            "npi_type": "Organization",
            "primary_practice_address": "456 Main St, Anytown, USA",
            "phone": "555-555-5556",
            "primary_taxonomy": "Dental"
        }

        # Deserialize the provider data
        provider_schema = ProviderSchema()
        provider = provider_schema.load(provider_data, session=db.session)
        self.assertEqual(provider.npi, "0987654321")
        self.assertEqual(provider.name, "Jane Doe")
    
    def test_provider_schema_serialization_only_npi(self):
        # Create a provider instance
        provider_data = {
            "npi": "0987654321",
        }
        provider_schema = ProviderSchema()
        provider = provider_schema.load(provider_data, session=db.session)
        self.assertEqual(provider.npi, "0987654321")