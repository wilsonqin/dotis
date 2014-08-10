from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from models.models import Donation
from mongoengine import *


import json
import pprint

#from lib.facebook import 

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
  
  #wrap redirect_url
  redirect_url = request.GET.get('r', False)


  context = {
    'title': 'Login to Dotis', 
    'redirect_url': redirect_url
    }
  return render(request, 'login.html', context)

# for ye ole relative url redirecting after post login
def redirect(request):
  print request
  context = {'title': 'Redirecting'}
  return redirect

def donation(request):
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







