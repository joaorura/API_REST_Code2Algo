
from mongoengine import Document, fields


class Methods(Document):
    name_of_method = fields.StringField(required=True)
    method_code = fields.ListField(fields.StringField(), required=True)
