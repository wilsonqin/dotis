from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json

def index(request):
	return render(request, 'map.html')