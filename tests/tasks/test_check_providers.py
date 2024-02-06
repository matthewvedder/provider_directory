import pytest
from flask_testing import TestCase
from app.app import create_app, db
from app.models.provider import Provider
from app.tasks.check_providers import update_provider_from_npi_single
from unittest.mock import patch



class TestUpdateProviderTask(TestCase):
    def create_app(self):
        # Return an instance of your Flask app with test configurations
        return create_app('test_config.py')

    def setUp(self):
        db.create_all()
        # Setup test data
        self.provider = Provider(npi="123456789", name="Test Provider")
        db.session.add(self.provider)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch('app.services.npi_registry.fetch_provider_from_registry')
    def test_update_provider_from_npi_single(self, mock_fetch):
        api_response = {
            "result_count": 1,
            "results": [{
                "number": "1205186715",
                "basic": {"organization_name": "24 ON PHYSICIANS, P.C."},
                "enumeration_type": "NPI-2",
                "addresses": [{
                    "address_1": "1500 S LAKE PARK AVE",
                    "city": "HOBART",
                    "state": "IN",
                    "postal_code": "463426638",
                    "telephone_number": "770-740-0895"
                }],
                "taxonomies": [{"desc": "Hospitalist"}]
            }]
        }

        # Mock the external service to return expected data
        mock_fetch.return_value = api_response

        # Run the task
        update_provider_from_npi_single(self.provider.id)

        # Reload the provider from the database
        updated_provider = Provider.query.get(self.provider.id)
        
        # Assertions
        self.assertEqual(updated_provider.name, 'Updated Provider Name', "Provider name should be updated.")
        # Add more assertions as needed to verify other fields are updated correctly
