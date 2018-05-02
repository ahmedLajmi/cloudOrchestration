from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
import json


@csrf_exempt
def list(request):
	services = Service.objects.all()
	compute = dict()
	db = dict()
	dbms = dict()
	webApp = dict()
	webServ = dict()
	soft = dict()
	cpt =0
	for service in services:
		cpt += 1
		if service.lie == "compute":
			compute.update({cpt:{"id":service.pk,'name':service.name}})
		if service.lie == "database":
			db.update({cpt:{"id":service.pk,'name':service.name}})
		if service.lie == "dbms":
			dbms.update({cpt:{"id":service.pk,'name':service.name}})
		if service.lie == "softwareComponent":
			soft.update({cpt:{"id":service.pk,'name':service.name}})
		if service.lie == "webApplication":
			webApp.update({cpt:{"id":service.pk,'name':service.name}})
		if service.lie == "webServer":
			webServ.update({cpt:{"id":service.pk,'name':service.name}})
		
	json_data = {"Compute":compute,"Database":db,"DBMS":dbms,"SoftwareComponent":soft,"WebApplication":webApp,"WebServer":webServ}
	json_data = json.dumps(json_data)
	return HttpResponse(json_data, content_type="application/json")

def calcul(request):
	req = request.POST.copy() 
	del req['csrfmiddlewaretoken']
	rcost = req['cost']
	del req['cost']
	ravab = req['availability']
	del req['availability']
	rtime = req['time']
	del req['time']
	cout=0
	disp = 99
	temps = 0
	cpt = 0
	for key,service in req.items():
		s= Service.objects.get(pk=service)
		cout += s.cout
		if cpt == 0:
			temps = s.temps
			cpt += 1
		elif s.temps >temps:
			temps = Service.objects.all()

	json_data = {"cost":cout,"time":temps,"disp":disp,'rcost':rcost,'ravab':ravab,'rtime':rtime}
	json_data = json.dumps(json_data)
	return HttpResponse(json_data, content_type="application/json")



