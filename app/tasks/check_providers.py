from app.app import db, create_app
from app.models.provider import Provider  # Adjust the import path according to your project structure
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

@celery.task
def update_provider_from_npi_single(provider_id):
    with app.app_context():
        try:
            provider = Provider.query.get(provider_id)
            if not provider:
                current_app.logger.error(f"Provider with ID {provider_id} not found.")
                return "Provider not found", False

            provider_data = fetch_provider_from_registry(provider.npi)
            if not provider_data:
                current_app.logger.error(f"Failed to fetch data for provider {provider.npi}.")
                return "Failed to fetch provider data from NPI registry", False

            serialized_data = serialize_registry_provider(provider_data)

            # Initialize a flag to track changes
            changes_made = False

            # Iterate through each key in the serialized data
            for key, new_value in serialized_data.items():
                # Check if the provider attribute exists to avoid AttributeError
                if hasattr(provider, key):
                    # Get the current value from the provider
                    current_value = getattr(provider, key, None)
                    # Compare the current value with the new value
                    if current_value != new_value:
                        # If different, update the provider attribute
                        setattr(provider, key, new_value)
                        changes_made = True
                        current_app.logger.info(f"Updated {key} for provider {Provider}.")

            if changes_made:
                # Only commit to the database if there were any changes
                db.session.commit()
                current_app.logger.info(f"Provider {Provider} updated successfully.")
                return f"Provider {Provider} updated successfully", True
            else:
                # No changes detected, no need to commit
                current_app.logger.info(f"No updates required for provider {Provider}.")
                return "No update needed", True

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating provider {Provider}: {e}")
            return f"Failed to update provider {Provider}: {e}", False

@celery.task
def update_providers_from_npi_batch():
    try:
        all_batches = get_provider_ids(batch_size=100)
        for batch_ids in all_batches:
            job = group(update_provider_from_npi_single.s(provider_id) for provider_id in batch_ids)
            job.apply_async()
            # Consider using job.get() if you wish to wait for results synchronously
        return "Batch update initiated successfully", True
    except Exception as e:
        current_app.logger.error(f"Error initiating batch update: {e}")
        return f"Failed to initiate batch update: {e}", False
    
def initiate_provider_updates():
    update_providers_from_npi_batch.delay()
    return "Batch update initiated successfully"
