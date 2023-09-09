from django.shortcuts import render
from django.http import HttpResponse
import json
# Create your views here.

def map_view(request):
    return render(request, "map/map_template.html")