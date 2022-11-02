import datetime
import mongoengine


class Dog(mongoengine.Document):
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    type = mongoengine.StringField()
    size = mongoengine.StringField(required=True)
    name = mongoengine.StringField(required=True)

    meta = {
        'db_alias': 'core',
        'collection': 'dogs'
    }
