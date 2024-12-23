from marshmallow import Schema, fields, validate


class EventSchema(Schema):
    """Schema para validação de eventos do calendário"""

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(validate=validate.Length(max=500))
    start = fields.DateTime(required=True)
    end = fields.DateTime()
    color = fields.Str(validate=validate.Length(max=7))
    all_day = fields.Boolean(default=False)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


event_schema = EventSchema()
events_schema = EventSchema(many=True)
