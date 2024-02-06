import requests
from flask import current_app

def fetch_provider_from_registry(npi):
    base_url = "https://npiregistry.cms.hhs.gov/api/"
    response = requests.get(base_url, params={"number": npi, "version": 2.1})
    if response.status_code == 200:
        return response.json()
    else:
        current_app.logger.error(f"Failed to fetch provider with NPI {npi}. Status code: {response.status_code}")
        return None

def serialize_registry_provider(provider_registry_response):
    provider_data = {}

    results = provider_registry_response.get('results', [])
    if results:
        provider = results[0]  # Assuming there's at least one result
        
        # Directly available fields
        if 'number' in provider:
            provider_data["npi"] = provider['number']
        if 'enumeration_type' in provider:
            provider_data["npi_type"] = provider['enumeration_type']

        # Fields inside 'basic'
        basic_info = provider.get('basic', {})
        if 'organization_name' in basic_info:
            provider_data["name"] = basic_info['organization_name']

        # Handling addresses
        addresses = provider.get('addresses', [])
        if addresses:
            primary_address = addresses[0]  # Assuming the first address is the primary one
            if 'address_1' in primary_address:
                provider_data["primary_practice_address"] = primary_address['address_1']
            if 'telephone_number' in primary_address:
                provider_data["phone"] = primary_address['telephone_number']

        # Handling taxonomies
        taxonomies = provider.get('taxonomies', [])
        if taxonomies:
            primary_taxonomy = taxonomies[0]  # Assuming the first taxonomy is the primary one
            if 'desc' in primary_taxonomy:
                provider_data["primary_taxonomy"] = primary_taxonomy['desc']

    return provider_data