from __future__ import division

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from models.models import Donation, User, Collection, populate_food_pantry, populate_collection_test

import json
import pprint

#from lib.facebook import 

from mongoengine.django.auth import MongoEngineBackend
from mongoengine.queryset import DoesNotExist
from django.contrib.auth import login as userlogin, authenticate
from mongoengine import *



def index(request):
  context = {'title': 'adsfsa'}
  return render(request, 'index.html', context)

def browse(request):
  context = {}
  return render(request, 'collections.html', context)

def collection(request, collection_id):
  # 53e78b9d3c47b1721c79b5d8
  # context = {'first_name': Collection.collector.first_name}
  return render(request, 'collection.html', context)

def users(request):
  context = {}
  return render(request, 'users.html', context)

def login(request):
  if(request.method == 'POST') and request.POST['usermail'] and request.POST['password']:
    redirect_url = request.POST.get('redirect_url', '/index')
    print 'redirect_url: ' + redirect_url
    #handle login attempt
    try:
      user = User.objects.get(email=request.POST['usermail'])
      if user.check_password(request.POST['password']):
          user.backend = 'mongoengine.django.auth.MongoEngineBackend'
          userlogin(request, user)

          # print 'login: user.is_authenticated: ' + request.user.is_authenticated()

          request.session.set_expiry(60 * 60 * 1) # 1 hour timeout

          print 'success logged in'
          
          #redirect to location if login success
          return redirect(redirect_url)
      else:
          return HttpResponse('login failed')
    except DoesNotExist:
        return HttpResponse('error, please check your username and password combination')
    #except Exception as e:
    #    print e
    #   return HttpResponse('unknown error')
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
      user = User(username=request.POST['emailsignup'], email=request.POST['emailsignup'], last_name=request.POST['lastnamesignup'], first_name=request.POST['firstnamesignup'], password=request.POST['passwordsignup'])
      user.init_password(request.POST['passwordsignup'])
      user.save()
      
      userlogin(request, user)
      request.session.set_expiry(60 * 60 * 1) # 1 hour timeout
      return HttpResponse("Registration")
    else:
        return HttpResponse('register failed, user already exists')
  else:
    return HttpResponse('nothing exists here')

def registerfb(request):
  return HttpResponse('fbregister')

def donation(request):
    #print 'request.user.is_authenticated=', request.user.is_authenticated()
    #if not request.user.is_authenticated():
    #  print 'on donation page, not authd '
    #  return redirect('/login?r=%s' % request.path)

    context = {'title': 'Donation'}
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
    pickup_location = { "type" : "Point" , "coordinates" : [float(request.POST['lat']), float(request.POST['lng'])]}
    donation_obj = Donation(name=name, donation_type=donation_type, weight=weight, description=description, estimated_value= estimated_value, item_count=item_count,
        pickup_location=pickup_location)

    print donation_obj.pickup_location
    donation_obj.save();


    # if request.POST['name'] and request.POST['donation_type'] and request.POST['item_count'] and request.POST['estimated_value']:
    #     donation = Donation(name=request.POST['name'], donation_type=request.POST['donation_type'], item_count=request.POST['item_count'], estimated_value= request.POST['estimated_value'])
    #     print donation.name
    #     print donation.donation_type
    # donation.save()
    return donation(request)

def map(request):
    context = {'title': 'Donations Map'}
    return render(request, 'map.html', context)

"""
 restful location data
 expects the request to have radius, latitude, longitude
"""
from bson.objectid import ObjectId
def getDonations(request):

    data = {}
    if request.GET['radius'] and request.GET['lat'] and request.GET['lng']:
        radius = float(request.GET['radius']) /  3963.192 #in radians
        lat = float(request.GET['lat'])
        lng = float(request.GET['lng'])
        places = Donation.objects(pickup_location__geo_within_center=[[lat, lng], radius ]);
        places_json = []
        for item in places:
            places_json.append({
                'name' : item.name,
                'donation_type' : item.donation_type,  
                'weight' : item.weight,
                'description' : item.description,
                'estimated_value' : item.estimated_value,
                'item_count' : item.item_count,
                'lat' : item.pickup_location['coordinates'][0],
                'lng' : item.pickup_location['coordinates'][1],
                'id' : str(item.id)
            });
    
        data = {
            'places': places_json
        }

    data = simplejson.dumps(data)
    return HttpResponse(data, content_type='application/json')

# """
#  restful location data
#  expects the request to have radius, latitude, longitude
# """
# from bson.objectid import ObjectId
# def getDonations(request):

#     data = {}
#     if request.GET['radius'] and request.GET['lat'] and request.GET['lng']:
#         radius = float(request.GET['radius']) /  3963.192 #in radians
#         lat = float(request.GET['lat'])
#         lng = float(request.GET['lng'])
#         places = DropoffLocation.objects(location__geo_within_center=[[lat, lng], radius ]);
#         places_json = []
#         for charity in places:
#             places_json.append({
#                 'name' : charity.charity.name,
#                 'donation_type' : charity.charity.types_accepted,
#                 'description' : charity.description,
#                 'lat' : charity.pickup_location['coordinates'][0],
#                 'lng' : charity.pickup_location['coordinates'][1],
#                 'id' : str(charity.id)
#             });
    
#         data = {
#             'places': places_json
#         }

#     data = simplejson.dumps(data)
#     return HttpResponse(data, content_type='application/json')

# def getCharities(request):
#   data = {}
#   if request.GET['radius'] and request.GET['lat'] and request.GET['lng']:
#       radius = float(request.GET['radius']) /  3963.192 #in radians
#       lat = float(request.GET['lat'])
#       lng = float(request.GET['lng'])
#       places = Charity.objects(pickup_location__geo_within_center=[[lat, lng], radius ]);
#       places_json = []
#       for item in places:
#           places_json.append({
#               'name' : item.name,
#               'donation_type' : item.donation_type,  
#               'weight' : item.weight,
#               'description' : item.description,
#               'estimated_value' : item.estimated_value,
#               'item_count' : item.item_count,
#               'lat' : item.pickup_location['coordinates'][0],
#               'lng' : item.pickup_location['coordinates'][1],
#               'id' : str(item.id)
#           });
  
#       data = {
#           'places': places_json
#       }

#   data = simplejson.dumps(data)
#   return HttpResponse(data, content_type='application/json')


def populate_food(request):
  populate_food_pantry()
  return HttpResponse("done")

def populate_collection(request):
  collection_id = populate_collection_test()
  return HttpResponse("collection created: " + str(collection_id))


def about(request):
  context = {}
  return render(request, 'about.html', context)
