from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json

import pprint


def index(request):
	context = {'title': 'adsfsa'}
	return render(request, 'index.html', context)

def login(request):
  context = {'title': 'Login to Dotis'}
  return render(request, 'login.html', context)

def manageDonation(request):
    context = {'title': 'Create Donation'}
    return render(request, 'donation.html', context)