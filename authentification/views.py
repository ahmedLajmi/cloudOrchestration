from django.shortcuts import render
from django.http import Http404
import datetime
import os
import time

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def home(request):
	return render(request , 'home.html')

def register(request):
	
	return render(request , 'register.html')


def login(request):
	
	return render(request , 'login.html')


def workspace(request):
	
	return render(request , 'workspace.html')


def formu(request):
	if len(request.POST) == 0:
		raise Http404("No MyModel matches the given query.")
	print (request.FILES)
	date = time.strftime('%d-%m-%y_%H-%M-%S',time.localtime())
	path = os.path.join(BASE_DIR, "userData\\")
	idUser = "1\\"
	path = path + idUser +"{}"+date+".yaml"
	originalToscaDefPath = BASE_DIR + "\\toscaparser\\elements\\TOSCA_definition_1_0.yaml"
	secureToscaDefPath = BASE_DIR + "\\toscaparser\\secure\\TOSCA_definition_1_0.yaml"
	toscaDefinition = request.FILES['toscaDefinition']
	toscaTemplate = request.FILES['toscaTemplate']
	# sauvegarder le tosca definition introduit par le client 
	with open(originalToscaDefPath, 'wb+') as definition:
		with open(path.format("toscaDef_"), 'wb+') as destination:
			for chunk in toscaDefinition.chunks():
				destination.write(chunk)
				definition.write(chunk)
	# sauvegarder le template tosca introduit par le client 
	with open(path.format("toscaTemplate"), 'wb+') as destination:
		for chunk in toscaTemplate.chunks():
			destination.write(chunk)
	# restaurer le tosca definition original
	with open(secureToscaDefPath, 'rb') as definition:
		with open(originalToscaDefPath, 'wb+') as destination:
			destination.write(definition.read())
	return render(request , 'workspace.html')

	
def graph(request):
	
	return render(request , 'graph.html')

