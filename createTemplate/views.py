from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json



@csrf_exempt
def list(request):
    json_data = json.dumps({"nodes":["compute"]})
    return HttpResponse(json_data, content_type="application/json")

