from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json

import pprint
from models.models import Donation

def index(request):
	context = {'title': 'adsfsa'}
	return render(request, 'index.html', context)

def login(request):
    context = {'title': 'Login to Dotis'}
    return render(request, 'login.html', context)

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