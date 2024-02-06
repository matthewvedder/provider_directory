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


# example response from api call:

# {
#   "result_count": 1,
#   "results": [
#     {
#       "created_epoch": "1347460995000",
#       "enumeration_type": "NPI-2",
#       "last_updated_epoch": "1459198967000",
#       "number": "1205186715",
#       "addresses": [
#         {
#           "country_code": "US",
#           "country_name": "United States",
#           "address_purpose": "LOCATION",
#           "address_type": "DOM",
#           "address_1": "1500 S LAKE PARK AVE",
#           "city": "HOBART",
#           "state": "IN",
#           "postal_code": "463426638",
#           "telephone_number": "770-740-0895",
#           "fax_number": "770-740-0896"
#         },
#         {
#           "country_code": "US",
#           "country_name": "United States",
#           "address_purpose": "MAILING",
#           "address_type": "DOM",
#           "address_1": "PO BOX 849318",
#           "city": "BOSTON",
#           "state": "MA",
#           "postal_code": "022849318",
#           "telephone_number": "770-740-0895",
#           "fax_number": "770-740-0896"
#         }
#       ],
#       "practiceLocations": [],
#       "basic": {
#         "organization_name": "24 ON PHYSICIANS, P.C.",
#         "organizational_subpart": "NO",
#         "enumeration_date": "2012-09-12",
#         "last_updated": "2016-03-28",
#         "status": "A",
#         "authorized_official_first_name": "DAN",
#         "authorized_official_last_name": "FULLER",
#         "authorized_official_middle_name": "A.",
#         "authorized_official_telephone_number": "7707400895",
#         "authorized_official_title_or_position": "VP/Secretary",
#         "authorized_official_name_prefix": "Mr.",
#         "authorized_official_name_suffix": "--"
#       },
#       "taxonomies": [
#         {
#           "code": "208M00000X",
#           "taxonomy_group": "193200000X - Multi-Specialty Group",
#           "desc": "Hospitalist",
#           "state": null,
#           "license": null,
#           "primary": true
#         }
#       ],
#       "identifiers": [],
#       "endpoints": [],
#       "other_names": []
#     }
#   ]
# }