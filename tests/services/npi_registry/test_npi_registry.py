import pytest
import requests_mock
from flask_testing import TestCase
from app.services.npi_registry import fetch_provider_from_registry, serialize_registry_provider
from app.app import create_app

# Example API response (simplified for brevity)
api_response = {
    "result_count": 1,
    "results": [{
        "number": "1205186715",
        "basic": {
            "authorized_official_first_name": "DAN",
            "authorized_official_last_name": "FULLER",
        },
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

class TestNPIService(TestCase):
    def create_app(self):
        # Return an instance of your Flask application configured for testing
        app = create_app('test_config.py')  # Adjust as necessary
        return app

    @requests_mock.Mocker()
    def test_fetch_provider_from_registry_success(self, m):
        # Mock the external API response
        npi_number = "1205186715"
        api_url = f"https://npiregistry.cms.hhs.gov/api/?number={npi_number}&version=2.1"
        m.get(api_url, json={"result_count": 1, "results": [{"number": npi_number}]})

        # Call your service function
        response = fetch_provider_from_registry(npi_number)
        self.assertIsNotNone(response)
        self.assertEqual(response['result_count'], 1)

    def test_serialize_registry_provider(self):
        # Prepare a mocked API response
        # Call your serialization function
        serialized_data = serialize_registry_provider(api_response)
        print(serialized_data)
        expected_data = {
            "npi": "1205186715",
            "name": "DAN FULLER",
            "npi_type": "NPI-2",
            "primary_practice_address": "1500 S LAKE PARK AVE",
            "city": "HOBART",
            "state": "IN",
            "postal_code": "463426638",
            "phone": "770-740-0895",
            "primary_taxonomy": "Hospitalist"
        }

        self.assertEqual(serialized_data, expected_data)
        