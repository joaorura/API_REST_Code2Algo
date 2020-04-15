
from mongoengine import Document, fields


class Methods(Document):
    method_name = fields.StringField(required=True)
    method_code = fields.StringField(required=True)
