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
        'indexes': [[("location", "2dsphere")]]
    }

class Donation(Document):
  donation_type = IntField(0)
  weight = IntField(0)
  estimated_value = IntField(0)
  item_count = IntField(0)
  pickup_location = PointField(auto_index=False)
  date = DateTimeField(default=datetime.datetime.now)
  status = IntField(0)
  collection_id = StringField()
  charity_id = StringField()


# collection of donation objects
class Collection(Document):
  user_id = StringField()
  donation_id_list = StringField()

# event of donation pick up / drop off
# status is 0 for donation created by user
# status is 0 for donation picked up by collector
# status is 0 for donation dropped off at charity by collector

class Transaction(Document):
  status = IntField()
  donation_id = StringField()
  user_id = StringField()
  date = DateTimeField(default=datetime.datetime.now)

