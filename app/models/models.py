from mongoengine import *

class Charity(Document):
  name = StringField()
  types_accepted = ListField()
  email = StringField(required=True)
  contact_name = StringField(required=True)

  meta = {
    # put an index on appropriate fields
    }

class DropoffLocation(Document):
  charity_id = StringField()
  location = PointField(auto_index=False)

  meta = {
        'indexes': [[("location", "2dsphere"), ("datetime", 1)]]
    }
