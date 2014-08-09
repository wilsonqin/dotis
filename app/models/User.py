from mongoengine import *
from hashlib import sha1 

class User(Document):
  email = StringField(required=True)
  first_name = StringField(required=True)
  last_name = StringField(required=True)
  zipcode = IntField(required=True)
  password = StringField(required=True)

  #add facebook oauth fields

  meta = {
    #put an index on email
    'indexes': [
      'email',
      'zipcode'
    ]
  }