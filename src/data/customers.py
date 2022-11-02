import datetime
import mongoengine

from data.surrenderings import DogSurrendering


class Customer(mongoengine.Document):
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    name = mongoengine.StringField(required=True)
    email = mongoengine.StringField(required=True)
    dog_names = mongoengine.ListField()
    surrendering = mongoengine.EmbeddedDocumentListField(DogSurrendering)
    meta = {
        'db_alias': 'core',
        'collection': 'customers'
    }
