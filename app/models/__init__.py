# from app import ma
# from app.models.provider import Provider
# from marshmallow import fields

# class ProviderSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Provider
#         load_instance = True  # Optional: deserialize to model instances

#     id = fields.Int(dump_only=True)
#     name = fields.Str(required=True)
#     service = fields.Str(required=True)