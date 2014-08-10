from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json

import pprint
from models.models import Donation
#from lib.facebook import 

def index(request):
  context = {'title': 'adsfsa', 'redirect_url': request.path}
  return render(request, 'index.html', context)

def browse(request):
  context = {}
  return render(request, 'collections.html', context)

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

def createDonation(request):
    context = {'title': 'Create Donation'}
    return render(request, 'donation.html', context)

# validate form elements and accept the form
def postCreateDonation(request):
    if request.POST['name'] and request.POST['donation_type'] and request.POST['item_count'] and request.POST['estimated_value']:
        donation = Donation(name=request.POST['name'], donation_type=request.POST['donation_type'], item_count=request.POST['item_count'], estimated_value= request.POST['estimated_value'])
        print donation.name
        print donation.donation_type

        # donation.save()
    return createDonation(request);
