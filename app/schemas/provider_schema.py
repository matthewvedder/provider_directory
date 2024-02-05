from app.app import ma, db
from app.models.provider import Provider  # Import the Provider model

class ProviderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Provider  # Specify the model it corresponds to
        load_instance = True  # Optional: deserialize to model instances
        sqla_session = db.session  # Provide SQLAlchemy session; required for SQLAlchemyAutoSchema
        include_fk = True  # Optional: set to True if you want foreign keys to be included in the schema
        load_only = ("id",)  # Fields to load only when deserializing, e.g., passwords
        dump_only = ("created_at", "updated_at")  # Fields to dump only when serializing