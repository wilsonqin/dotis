import simplejson as json

import sys, os

here = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.normpath(os.path.join(here, '../app/')))

from mongoengine import connect

from models.models import DropoffLocation, Charity


PROD = False

f = open('../data/boston-food-pantries.json')
buf = f.read()


data = json.loads(str(buf))

data = data['data']

if PROD:
    connect('app28313994', username='test', password='abctest', host='kahana.mongohq.com', port=10043)
else:
    connect('dotis')

for pantry in data:
  pid = pantry[8]
  name = pantry[9]
  geo_list = pantry[11]

  site = pantry[14]
  print site

  address = geo_list[0]
  lati = float(geo_list[1])
  longi = float(geo_list[2])

  address_pts = json.loads(address)

  address = address_pts['address'] + ', ' + address_pts['city'] + ', ' + address_pts['state'] + " " + address_pts['zip']

  print address, pid, name, lati, longi

  charity = Charity(id=pid, name=name, types_accepted=[3])
  dropoff_loc = DropoffLocation(description=address, charity=pid, location=[lati, longi], url=site)
  charity.save()
  dropoff_loc.save()

