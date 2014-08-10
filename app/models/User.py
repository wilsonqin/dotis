from mongoengine import *
from hashlib import sha1 

user_types = ["native", "facebook", "google"]

class User(Document):
  email = StringField(required=True)
  first_name = StringField(required=True)
  last_name = StringField(required=True)
  zipcode = IntField(required=True)
  password = StringField(required=True)

  # account types: "native", "facebook", "google"
  account_type = StringField(required=True, default="native")

  #add facebook oauth fields
  facebook_id = StringField()
  friends = ListField(StringField())

  meta = {
    #put an index on email
    'indexes': [
      'email',
      'zipcode'
    ]
  }
