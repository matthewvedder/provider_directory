from flask import Blueprint, request, jsonify
from app.models.provider import Provider
from app.schemas.provider_schema import ProviderSchema
from app.app import db
from marshmallow.exceptions import ValidationError
from sqlalchemy import exc

provider_blueprint = Blueprint('providers', __name__)
provider_schema = ProviderSchema()
providers_schema = ProviderSchema(many=True)

@provider_blueprint.route('/providers', methods=['POST'])
def add_provider():
    provider_schema = ProviderSchema()
    try:
        # Validate and deserialize input
        provider= provider_schema.load(request.json, session=db.session)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Add to the database and commit
    db.session.add(provider)
    try:
        db.session.commit()
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'NPI must be unique'}), 400

    # Serialize and return the newly created provider
    return provider_schema.jsonify(provider), 201

