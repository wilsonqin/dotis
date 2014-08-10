from mongoengine import *
import datetime

#remember our User model is in its own file
from User import User

class Charity(Document):
  name = StringField()
  types_accepted = ListField()
  email = StringField(required=True)
  contact_name = StringField(required=True)

  meta = {
    # put an index on appropriate fields
    }

class DropoffLocation(Document):
  charity = ReferenceField('Charity')
  location = PointField(auto_index=False)

  meta = {
        'indexes': [[("location", "2dsphere")]]
    }

class Donation(Document):
  name = StringField()
  donation_type = IntField(0)
  weight = IntField(0)
  estimated_value = IntField(0)
  # item_count = IntField(0)
  # pickup_location = PointField(auto_index=False)
  # date = DateTimeField(default=datetime.datetime.now)
  # status = IntField(0)
  # collection_id = StringField()
  # charity_id = StringField()

pledge_status = ["pending", "done"]

class Pledge(Document):
  donation = ReferenceField('Donation')
  user = ReferenceField('User')
  amount = FloatField(0)
  status = StringField(default="pending")
  date_pledged = DateTimeField(default=datetime.datetime.now)

# collection of donation objects
class Collection(Document):
  collector = ReferenceField('User')
  donation_list = ListField(ReferenceField('Donation'))
  donors = ListField(ReferenceField('User'))
  date_committed = DateTimeField(default=datetime.datetime.now)

# event of donation pick up / drop off
# status is 0 for donation created by user
# status is 0 for donation picked up by collector
# status is 0 for donation dropped off at charity by collector

transaction_status = ["created", "picked_up", "dropped_off"]

class Transaction(Document):
  status = StringField()
  donation = ReferenceField('Donation')
  user = ReferenceField('User')
  date = DateTimeField(default=datetime.datetime.now)

