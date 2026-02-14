from marshmallow import Schema, fields, validate

class RankingSchema(Schema):
    ano = fields.Int(
        required=True,
        validate=validate.OneOf([2022, 2023, 2024])
    )
