from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json

def index(request):
	context = {'title': 'adsfsa'}
	return render(request, 'index.html', context)

def login(request):
  context = {'title': 'Login to Dotis'}
  return render(request, 'login.html', context)

def createDonation(request):
	context = {'title': 'Create Donation'}
	return render(request, 'donation.html', context)