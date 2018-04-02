from _sitebuiltins import _Printer

from django.shortcuts import render
from nodePerso.models import BaseNode
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json



@csrf_exempt
def list(request):
    nodes = dict()
    for baseNode in BaseNode.objects.all():
        nodes.update({baseNode.name : 'b'+str(baseNode.pk)})
    for persoNode in request.user.nodepersonalised_set.all():
        nodes.update({persoNode.name: 'p' + str(persoNode.pk)})
    print(nodes)
    json_data = json.dumps(nodes)
    return HttpResponse(json_data, content_type="application/json")

