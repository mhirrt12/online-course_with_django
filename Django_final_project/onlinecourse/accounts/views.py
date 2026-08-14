from http.client import HTTPResponse

from django.shortcuts import render

# Create your views here.
def register(request):
   return HTTPResponse("This is the register view.")
