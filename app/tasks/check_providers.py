from app.app import db, create_app
from app.models.provider import Provider  # Adjust the import path according to your project structure
from app.schemas.provider_schema import ProviderSchema
from app.services.npi_registry import fetch_provider_from_registry, serialize_registry_provider
from celery import group
from flask import current_app
app = create_app()
celery = app.celery # Pass your Flask app instance

def get_provider_ids(batch_size=100):
    """Yield batches of provider IDs from the database."""
    total = Provider.query.count()
    for offset in range(0, total, batch_size):
        batch_ids = Provider.query.with_entities(Provider.id).order_by(Provider.id).offset(offset).limit(batch_size).all()
        yield [id[0] for id in batch_ids]

from flask import current_app
from app.app import db, create_app
from app.models.provider import Provider  # Adjust the import path according to your project structure
from app.schemas.provider_schema import ProviderSchema
from app.services.npi_registry import fetch_provider_from_registry
from celery import Celery

app = create_app()
celery = app.celery

@celery.task
def update_provider_from_npi_single(provider_id):
    with app.app_context():
        provider_schema = ProviderSchema()
        try:
            provider = Provider.query.get(provider_id)
            if not provider:
                current_app.logger.error(f"Provider with ID {provider_id} not found.")
                return "Provider not found", False

            provider_data = fetch_provider_from_registry(provider.npi)
            if not provider_data:
                current_app.logger.error(f"Failed to fetch data for provider with NPI: {provider.npi}.")
                return "Failed to fetch provider data from NPI registry", False

            serialized_data = provider_schema.dump(provider)
            updated_data = provider_schema.load(provider_data, instance=provider, partial=True)

            # Check if there are any changes
            if serialized_data == updated_data:
                current_app.logger.info(f"No updates required for provider {provider_id}.")
                return "No update needed", True

            # Archive the provider if changes are detected
            provider.archive()

            # Apply the loaded data to the provider instance
            db.session.commit()
            current_app.logger.info(f"Provider {provider_id} updated successfully.")
            return f"Provider {provider_id} updated successfully", True

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating provider {provider_id}: {e}")
            return f"Failed to update provider {provider_id}: {e}", False

@celery.task
def update_providers_from_npi_batch():
    try:
        all_batches = get_provider_ids(batch_size=100)
        for batch_ids in all_batches:
            job = group(update_provider_from_npi_single.s(provider_id) for provider_id in batch_ids)
            job.apply_async()
        return "Batch update initiated successfully", True
    except Exception as e:
        current_app.logger.error(f"Error initiating batch update: {e}")
        return f"Failed to initiate batch update: {e}", False
    
def initiate_provider_updates():
    update_providers_from_npi_batch.delay()
    return "Batch update initiated successfully"
