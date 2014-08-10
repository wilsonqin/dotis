from mongoengine import *
import datetime

#remember our User model is in its own file
from User import User

donation_types = ["clothes", "furniture", "books"]

class Charity(Document):
  name = StringField()
  types_accepted = ListField(IntField(min_value=0))
  email = StringField(required=True)
  contact_name = StringField(required=True)

  meta = {
    # put an index on appropriate fields
    'indexes': ['name', 'types_accepted']
  }

donation_status = ["open", "done"]

class Donation(Document):
  name = StringField()
  donation_type = IntField(min_value=0)
  weight = IntField(min_value=0)
  description = StringField()
  estimated_value = FloatField(min_value=0)
  user = ReferenceField('User')
  item_count = IntField(min_value=0)
  pickup_location = PointField(auto_index=False)
  pickup_date_start = DateTimeField(default=datetime.datetime.now)
  # pickup_date_end = DateTimeField(default=(datetime.datetime.now + datetime.timedelta(days=3)))
  # collection_id = StringField()
  # charity_id = StringField()

  meta = {
    'indexes': [[("pickup_location", "2dsphere"), ("pickup_date_start", 1)]]
  }



pledge_status = ["pending", "done"]

class Pledge(Document):
  donation = ReferenceField('Donation')
  user = ReferenceField('User')
  amount = FloatField(min_value=0)
  status = StringField(default="pending")
  date_pledged = DateTimeField(default=datetime.datetime.now)

  meta = {
        'indexes': ["donation", "user", "status", "date_pledged"]
    }

# collection of donation objects
class Collection(Document):
  collector = ReferenceField('User')
  donation_list = ListField(ReferenceField('Donation'))
  donors = ListField(ReferenceField('User'))
  date_committed = DateTimeField(default=datetime.datetime.now)

  meta = {
      'indexes': ["collector", "donation_list", "date_committed"]
  }

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

  meta = {
        'indexes': ["user", "date"]
    }


def create_indexes():
  User.ensure_indexes()
  Charity.ensure_indexes()
  DropoffLocation.ensure_indexes()
  Donation.ensure_indexes()
  Pledge.ensure_indexes()
  Collection.ensure_indexes()
  Transaction.ensure_indexes()
