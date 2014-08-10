from mongoengine import *
import datetime
import json

from random import uniform, random, randint

from django.conf import settings

#remember our User model is in its own file
from User import User

donation_types = ["clothes", "furniture", "books", "food"]

class Charity(Document):
  name = StringField()
  types_accepted = ListField(IntField(min_value=0))
  email = StringField()
  contact_name = StringField()

  meta = {
    # put an index on appropriate fields
    'indexes': ['name', 'types_accepted']
  }

class DropoffLocation(Document):
  charity = ReferenceField('Charity')
  location = PointField(auto_index=False) # [x = lat, y = long]
  description = StringField()
  url = StringField()

  meta = {
        'indexes': [[("location", "2dsphere")], 'charity']
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

# collection of donation objects
class Collection(Document):
  collector = ReferenceField('User')
  donation_list = ListField(ReferenceField('Donation'))
  donors = ListField(ReferenceField('User'))
  date_committed = DateTimeField(default=datetime.datetime.now)

  meta = {
      'indexes': ["collector", "donation_list", "date_committed"]
  }

pledge_status = ["pending", "done"]

class Pledge(Document):
  collection = ReferenceField('Collection')
  user = ReferenceField('User')
  amount = FloatField(min_value=0)
  status = StringField(default="pending")
  date_pledged = DateTimeField(default=datetime.datetime.now)

  meta = {
        'indexes': ["collection", "user", "status", "date_pledged"]
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

def create_test_user(identifier):
  try:
    user = User.objects.get(email=identifier+"test@test.com")
  except:
    user = User(email=identifier+"test@test.com", username=identifier+"test@test.com", password="test", first_name=identifier, last_name="Tester")
    user.init_password("test")
    user.save()
  
  return user.id;

def populate_collection_test():
  uids = [create_test_user('bob'), create_test_user('sally')]
  collector_id = create_test_user('batman')

  for uid in uids:
    donation_ids = []
    for i in range(0,7,1):
      coord = [42.352663 + uniform(-0.2, 0.2), -71.0675998 + uniform(-0.2, 0.2)]
      donation = Donation(user=uid, estimated_value=20.00 + uniform(0.0, 10.0), name="Food Donation",description="lots of canned food", pickup_location=coord, weight=randint(0,15), donation_type=3)
      donation.save()
      donation_ids.append(donation.id)

  #create collection
  collection = Collection(donors=uids, donation_list=donation_ids, collector=collector_id)
  collection.save()
  collection_id = collection.id

  uids = [create_test_user('greg'), create_test_user('julia')]
  for uid in uids:
    for i in range(0,5,1):
      Pledge(collection=collection_id, user=uid, amount=uniform(1.0,500.0))

  return collection_id


def populate_food_pantry():
  Charity.drop_collection()
  DropoffLocation.drop_collection()

  BASE_DIR = getattr(settings, "BASE_DIR", None)

  f = open(BASE_DIR + '/app/models/data/boston-food-pantries.json', 'r')
  buf = f.read()
  data = json.loads(str(buf))
  data = data['data']

  for pantry in data:
    name = pantry[9]
    geo_list = pantry[11]

    site = pantry[14]
    # print site

    address = geo_list[0]
    lati = float(geo_list[1])
    longi = float(geo_list[2])

    address_pts = json.loads(address)

    address = address_pts['address'] + ', ' + address_pts['city'] + ', ' + address_pts['state'] + " " + address_pts['zip']

    # print address, pid, name, lati, longi

    charity = Charity(name=name, types_accepted=[3])
    charity.save()
    pid = charity.id
    dropoff_loc = DropoffLocation(description=address, charity=pid, location=[lati, longi], url=site)
    dropoff_loc.save()

  Charity.ensure_indexes()
  DropoffLocation.ensure_indexes()