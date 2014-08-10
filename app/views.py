from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import json

def index(request):
	context = {'title': 'adsfsa'}
	return render(request, 'index.html', context)