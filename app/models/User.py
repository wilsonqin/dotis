from mongoengine import *
from hashlib import sha1 

user_types = ["native", "facebook", "google"]

class User(Document):
  email = StringField(required=True)
  first_name = StringField(required=True)
  last_name = StringField(required=True)
  zipcode = IntField()
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

  def check_password(self, plaintxt_password):
    hash_obj = sha1(plaintxt_password)
    return (hash_obj.hexdigest() == self.password)

  #only call when first time setting a new password
  def init_password(self, plaintxt_password):
    hash_obj = sha1(plaintxt_password)
    self.password = hash_obj.hexdigest()
