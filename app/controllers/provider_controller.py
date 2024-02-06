from flask import Blueprint, request, jsonify, current_app as app
from app.models.provider import Provider
from app.models.provider_archive import ProviderArchive
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
        provider = provider_schema.load(request.json, session=db.session)
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

@provider_blueprint.route('/providers', methods=['GET'])
def get_providers():
    try:
        all_providers = Provider.query.all()
        return providers_schema.jsonify(all_providers), 200
    except exc.SQLAlchemyError as e:
        # Log the error for debugging purposes
        app.logger.error(f"Database error occurred: {str(e)}")
        return jsonify({'error': 'Could not fetch providers due to a database error.'}), 500

@provider_blueprint.route('/archived_providers', methods=['GET'])
def get_archived_providers():
    try:
        all_archived_providers = ProviderArchive.query.all()
        return providers_schema.jsonify(all_archived_providers), 200
    except exc.SQLAlchemyError as e:
        # Log the error for debugging purposes
        app.logger.error(f"Database error occurred: {str(e)}")
        return jsonify({'error': 'Could not fetch archived providers due to a database error.'}), 500

@provider_blueprint.route('/providers/stats', methods=['GET'])
def get_provider_stats():
    try:
        total_providers = Provider.query.count()
        total_archived = ProviderArchive.query.count()
        total_updated = Provider.query.filter(Provider.updated_at != Provider.created_at).count()
        
        return jsonify({
            'total_providers': total_providers,
            'total_archived': total_archived,
            'total_updated': total_updated,
            'percentage_updated': f'{(total_updated / total_providers) * 100:.2f}%'
        }), 200
    except exc.SQLAlchemyError as e:
        # Log the error for debugging purposes
        app.logger.error(f"Database error occurred: {str(e)}")
        return jsonify({'error': 'Could not fetch provider statistics due to a database error.'}), 500
    except Exception as e:
        # Catch any other unexpected errors
        app.logger.error(f"Unexpected error occurred: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred.'}), 500

