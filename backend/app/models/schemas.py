"""
Cattle MongoDB Schema / Model Helper
Author: Akash
"""

from marshmallow import Schema, fields, validate


class CattleSchema(Schema):
    """Validation schema for cattle documents."""
    tag_id = fields.Str(required=True)
    name = fields.Str()
    breed = fields.Str(required=True, validate=validate.OneOf([
        "Gir", "Sahiwal", "Red Sindhi", "Tharparkar", "Ongole", "Kangayam", "Deoni", "Other"
    ]))
    age_years = fields.Float()
    weight_kg = fields.Float()
    owner_id = fields.Str()
    farm_id = fields.Str()
    health_status = fields.Str(validate=validate.OneOf(["healthy", "sick", "critical", "deceased"]))


class SensorReadingSchema(Schema):
    """Validation schema for sensor readings."""
    cattle_id = fields.Str(required=True)
    farm_id = fields.Str(required=True)
    sensor_type = fields.Str(required=True, validate=validate.OneOf([
        "temperature", "heartrate", "gps", "activity"
    ]))
    data = fields.Dict(required=True)
    device_id = fields.Str()
    timestamp = fields.DateTime()
