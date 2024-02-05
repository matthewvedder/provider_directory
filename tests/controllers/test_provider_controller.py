from flask_testing import TestCase
from app.app import create_app, db
from app.models.provider import Provider

class TestProviderEndpoints(TestCase):
    # Existing setup and teardown methods...
    def create_app(self):
        # Return an instance of your Flask application configured for testing
        return create_app('test_config.py')

    def setUp(self):
        # Create the database and tables
        db.create_all()

    def tearDown(self):
        # Drop all tables and remove session
        db.session.remove()
        db.drop_all()

    def test_add_provider(self):
        # Data for creating a new provider
        new_provider_data = {
            "npi": "1234567890",
            "name": "John Doe",
            "npi_type": "Individual",
            "primary_practice_address": "123 Main St, Anytown, USA",
            "phone": "555-555-5555",
            "primary_taxonomy": "General Practice"
        }

        # Send a POST request to the add_provider endpoint
        response = self.client.post('/providers', json=new_provider_data)

        # Check that the response status code is 201 (Created)
        self.assertEqual(response.status_code, 201)

        # Deserialize the response data and verify the provider was added correctly
        response_data = response.json
        self.assertEqual(response_data['npi'], new_provider_data['npi'])
        self.assertEqual(response_data['name'], new_provider_data['name'])

        # Verify the provider was added to the database
        provider = Provider.query.first()
        self.assertIsNotNone(provider)
        self.assertEqual(provider.npi, new_provider_data['npi'])

    def test_add_provider_duplicate_npi(self):
        # Data for creating a new provider
        new_provider_data = {
            "npi": "1234567890",
            "name": "John Doe",
            "npi_type": "Individual",
            "primary_practice_address": "123 Main St, Anytown, USA",
            "phone": "555-555-5555",
            "primary_taxonomy": "General Practice"
        }

        # Add the provider to the database
        provider = Provider(**new_provider_data)
        db.session.add(provider)
        db.session.commit()

        # Send a POST request to the add_provider endpoint with the same NPI
        response = self.client.post('/providers', json=new_provider_data)

        # Check that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

        # Verify the response contains an error message
        response_data = response.json
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'NPI must be unique')