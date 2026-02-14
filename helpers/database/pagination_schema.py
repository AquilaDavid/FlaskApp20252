from marshmallow import Schema, fields, validate

class PaginationSchema(Schema):
    page = fields.Int(
        load_default=1,
        validate=validate.Range(min=1)
    )
    limit = fields.Int(
        load_default=10,
        validate=validate.Range(min=1, max=100)
    )
