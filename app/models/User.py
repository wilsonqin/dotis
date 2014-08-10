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
    m = md5()
    m.update(plaintxt_password)
    return (m.digest() == password)

  #only call when first time setting a new password
  def init_password(self, plaintxt_password):
    m = md5()
    m.update(plaintxt_password)
    self.password = m.digest()
