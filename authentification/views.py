from django.shortcuts import render
from django.http import Http404

import importlib
import datetime
import os
import time
import sys

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
	os.utime("C:\\Users\\ahlaj\Desktop\\cloudOrchestration\\toscaparser\\tosca_template.py", (time.time(),time.time()))
	now = datetime.datetime.now()
	after = now.replace(second=now.second+5)
	"""with open("C:\\Users\\ahlaj\Desktop\\cloudOrchestration\\toscaparser\\auxiliare.py", 'rb+') as source:
		with open("C:\\Users\\ahlaj\Desktop\\cloudOrchestration\\toscaparser\\tosca_template.py", 'wb+') as destination:
			destination.write(source.read())"""
	
	"""if(importlib.reload(tosca_template)):
		print ('it s ok')"""
	#import toscaparser.tosca_template as ToscaTemplate
	while (datetime.datetime.now() < after):
		print('heloo')

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
	toscaTemplat = request.FILES['toscaTemplate']
	# sauvegarder le tosca definition introduit par le client 
	with open(path.format("toscaDef_"), 'wb+') as destination:
		for chunk in toscaDefinition.chunks():
			destination.write(chunk)
	with open(originalToscaDefPath, 'wb+') as definition:
		for chunk in toscaDefinition.chunks():
			definition.write(chunk)
	# sauvegarder le template tosca introduit par le client 
	with open(path.format("toscaTemplate"), 'wb+') as destination:
		for chunk in toscaTemplat.chunks():
			destination.write(chunk)
	from toscaparser import tosca_template
	#return render(request , 'workspace.html')
    # path1 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lib/tosca_parser/tosca_parser.py')     
	"""importlib.invalidate_caches()
	ToscaTemplate = importlib.import_module('toscaparser.tosca_template')
	importlib.reload(ToscaTemplate)"""

	

	#importlib.reload(toscaparser.tosca_template)
	temp = tosca_template.ToscaTemplate(path.format("toscaTemplate"))

	
	graphe = temp.graph
	nodes = graphe.nodetemplates
	mon_fichier = open(path.format("toscaTemplate"), "r")
	file = mon_fichier.read()
	cpt = 0
	id_node = 0
	noeuds = dict()
	rel = dict()
	nature = str()
	src = 0
	for noeud in nodes:
		noeuds[id_node] = {'name': noeud.name,'type':noeud.type.replace("tosca.nodes.",'') }
		id_node = id_node+1
	for noeud in nodes:
		for require in noeud.requirements:
			for key in require.keys():
				if(key == "host"):

					for cle,val in noeuds.items():
						if val["name"] == require.get(key):
							dest = cle
						if val["name"] == noeud.name:
							src = cle

					rel[cpt] = {'type': 'hostedOn','nsrc':noeud.name ,'ndest':require.get(key) ,'source':src, 'dest':dest}
					cpt = cpt+1
				else:
					values = require.get(key)
					for value in values:
						if (value == "node"):

							for cle,val in noeuds.items():
								if val["name"] == values.get(value):
									dest = cle
								if val["name"] == noeud.name:
									src = cle

						if (value == "relationship"):
							nature = values.get(value).replace("tosca.relationships.",'')
					rel[cpt] = {'type': nature,'nsrc':noeud.name ,'ndest':require.get(key) ,'source':src , 'dest':dest}
					cpt = cpt+1
	# restaurer le tosca definition original
	"""with open(secureToscaDefPath, 'rb') as definition:
		with open(originalToscaDefPath, 'wb+') as destination:
			destination.write(definition.read())"""

	return render(request , 'graph.html',{'noeuds': noeuds,'relations':rel, 'file':file})

	
	

def delete_module(modname, paranoid=None):
    from sys import modules
    try:
        thismod = modules[modname]
    except KeyError:
        raise ValueError(modname)
    these_symbols = dir(thismod)
    if paranoid:
        try:
            paranoid[:]  # sequence support
        except:
            raise ValueError('must supply a finite list for paranoid')
        else:
            these_symbols = paranoid[:]
    del modules[modname]
    for mod in modules.values():
        try:
            delattr(mod, modname)
        except AttributeError:
            pass
        if paranoid:
            for symbol in these_symbols:
                if symbol[:2] == '__':  # ignore special symbols
                    continue
                try:
                    delattr(mod, symbol)
                except AttributeError:
                    pass