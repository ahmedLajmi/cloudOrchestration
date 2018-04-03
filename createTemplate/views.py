from _sitebuiltins import _Printer

from django.shortcuts import render
from nodePerso.models import BaseNode
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms import formset_factory
from .forms import ComputeForm,DatabaseForm
import json



@csrf_exempt
def list(request):
    nodes = dict()
    for baseNode in BaseNode.objects.all():
        nodes.update({baseNode.name : 'b'+str(baseNode.pk)})
    for persoNode in request.user.nodepersonalised_set.all():
        nodes.update({persoNode.name: 'p' + str(persoNode.pk)})
    json_data = json.dumps(nodes)
    return HttpResponse(json_data, content_type="application/json")

def form(request):
    for element in request.POST:
        if("node" in element):
            print(request.POST[element])
            print(request.POST["num"+element.replace("node","")])
    computeFormset = formset_factory(ComputeForm , extra=2)
    computeForm = computeFormset()
    forms = (ComputeForm(),DatabaseForm())
    return render(request, 'createTemplate/form.html', {'form': computeForm})

@csrf_exempt
def loadDist(request):
    windowsDistribution = {"windowsXp" : "Windows Xp", "windows7" :"Windows 7", "windows10" :"Windows 10"}
    linuxDistribution = {"ubuntu" : "Ubuntu", "mint" :"Mint"}
    print(request.POST["type"])
    if(request.POST["type"] == "windows"):
        distribution = windowsDistribution
    else:
        distribution = linuxDistribution
    json_data = json.dumps(distribution)
    return HttpResponse(json_data, content_type="application/json")

def validateForm(request):
    return HttpResponse("hello")