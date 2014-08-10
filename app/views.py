from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from models.models import Donation, User

import json
import pprint

#from lib.facebook import 

from mongoengine.django.auth import MongoEngineBackend
from mongoengine.queryset import DoesNotExist
from django.contrib.auth import login as userlogin



def index(request):
  context = {'title': 'adsfsa', 'redirect_url': request.path}
  return render(request, 'index.html', context)

def browse(request):
  context = {}
  return render(request, 'collections.html', context)

def users(request):
  context = {}
  return render(request, 'users.html', context)

def login(request):
  if(request.method == 'POST') and request.POST['usermail'] and request.POST['password']:
    #handle login attempt
    try:
      user = User.objects.get(email=request.POST['usermail'])
      if user.check_password(request.POST['password']):
          user.backend = 'mongoengine.django.auth.MongoEngineBackend'
          userlogin(request, user)
          request.session.set_expiry(60 * 60 * 1) # 1 hour timeout
          return HttpResponse(user)
      else:
          return HttpResponse('login failed')
    except DoesNotExist:
        return HttpResponse('error, please check your username and password combination')
    except Exception:
        return HttpResponse('unknown error')
  else:
    #render login form

    #wrap redirect_url
    redirect_url = request.GET.get('r', False)

    context = {
      'title': 'Login to Dotis', 
      'redirect_url': redirect_url
      }
    return render(request, 'login.html', context)

#for regular register
def register(request):
  if(request.method == 'POST') and request.POST['emailsignup']:
    #handle login attempt
    try:
      user = User.objects.get(email__exact=request.POST['emailsignup'])
    except DoesNotExist:
      user = None
    if not user:
      user = User(email=request.POST['emailsignup'], last_name=request.POST['lastnamesignup'], first_name=request.POST['firstnamesignup'], password=request.POST['passwordsignup'])
      user.init_password(request.POST['passwordsignup'])
      user.save()
      
      user.backend = 'mongoengine.django.auth.MongoEngineBackend'
      userlogin(request, user)
      request.session.set_expiry(60 * 60 * 1) # 1 hour timeout
      return HttpResponse(user)
    else:
        return HttpResponse('register failed, user already exists')
  else:
    return HttpResponse('nothing exists here')

def registerfb(request):
  return HttpResponse('fbregister')

<<<<<<< HEAD
def donation(request):
    context = {'title': 'Donation'}
=======
def createDonation(request):
    if not request.user.is_authenticated():
      return redirect('/login?r=%s' % request.path)

    context = {'title': 'Create Donation'}
>>>>>>> 752966cf104a946370b69d27484af9157710b832
    return render(request, 'donation.html', context)

# validate form elements and accept the form
def createDonation(request):
    print request.POST
    name = request.POST['name']
    donation_type = request.POST['donation_type']
    weight = request.POST['weight']
    description = "my description"
    estimated_value = request.POST['estimated_value']
    # user = request.POST['user_id'] 
    item_count = request.POST['item_count']
    pickup_location = { "type" : "Point" , "coordinates" : [request.POST['lat'], request.POST['lng']]}
    donation_obj = Donation(name=name, donation_type=donation_type, weight=weight, description=description, estimated_value= estimated_value, item_count=item_count,
        pickup_location=pickup_location)

    print donation_obj.pickup_location


    # if request.POST['name'] and request.POST['donation_type'] and request.POST['item_count'] and request.POST['estimated_value']:
    #     donation = Donation(name=request.POST['name'], donation_type=request.POST['donation_type'], item_count=request.POST['item_count'], estimated_value= request.POST['estimated_value'])
    #     print donation.name
    #     print donation.donation_type
    # donation.save()
    return donation(request)

def map(request):
    context = {'title': 'Map'}
    return render(request, 'map.html', context)

"""
 restful location data
 expects the request to have radius, latitude, longitude
"""
# def getDonations(request):
#     data = {
#        'test': 1
#     }

#     data = simplejson.dumps(data)
#     # if request.POST['radius'] and request.POST['lat'] and request.POST['lng']:
#     #     radius = request.POST['radius']
#     #     latitude = request.POST['lat']
#     #     longitude = request.POST['lng']
#     # else:
#     db.places.find( { 
#         loc: { $geoWithin :
#               { $center : [ [-74, 40.74], 10 ] }
#     } } )

#     return HttpResponse(data, mimetype='application/json')







