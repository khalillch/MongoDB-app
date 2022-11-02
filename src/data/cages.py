import datetime
import mongoengine


class Cage(mongoengine.Document):
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    size = mongoengine.StringField(required=True)
    is_used = mongoengine.BooleanField(default=False)
    dog_id = mongoengine.ObjectIdField()

    meta = {
        'db_alias': 'core',
        'collection': 'cages'
    }
