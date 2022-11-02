import datetime
import mongoengine


class DogSurrendering(mongoengine.EmbeddedDocument):
    prev_owner_id = mongoengine.ObjectIdField()
    dog_ids = mongoengine.ListField()
    surrendering_date = mongoengine.DateTimeField(default=datetime.datetime.now)

    meta = {
        'db_alias': 'core',
        'collection': 'dog_surrendering'
    }
