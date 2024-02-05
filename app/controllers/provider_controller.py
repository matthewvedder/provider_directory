from flask import Blueprint, request, jsonify
from app.models.provider import Provider
from app.schemas.provider_schema import ProviderSchema
from app.app import db

provider_blueprint = Blueprint('providers', __name__)
provider_schema = ProviderSchema()
providers_schema = ProviderSchema(many=True)

@provider_blueprint.route('/providers', methods=['POST'])
def add_provider():
    name = request.json['name']
    service = request.json['service']
    provider = Provider(name, service)
    db.session.add(provider)
    db.session.commit()
    return provider_schema.jsonify(provider)

@provider_blueprint.route('/providers', methods=['GET'])
def get_providers():
    all_providers = Provider.query.all()
    result = providers_schema.dump(all_providers)
    return jsonify(result)
