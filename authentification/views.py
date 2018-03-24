from django.shortcuts import render
from django.http import Http404
from toscaparser.tosca_template import ToscaTemplate
import importlib
import datetime
import os
import time
import sys

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def register(request):
	with open(BASE_DIR+'\\static\\about.txt', 'r') as source:
		about = source.read()
	with open(BASE_DIR+'\\static\\privacy.txt', 'r') as source:
		privacy = source.read()
	with open(BASE_DIR+'\\static\\term.txt', 'r') as source:
		term = source.read()
	return render(request , 'register.html',{'about': about,'privacy':privacy, 'term':term})


def login(request):
	with open(BASE_DIR+'\\static\\about.txt', 'r') as source:
		about = source.read()
	with open(BASE_DIR+'\\static\\privacy.txt', 'r') as source:
		privacy = source.read()
	with open(BASE_DIR+'\\static\\term.txt', 'r') as source:
		term = source.read()
	return render(request , 'login.html',{'about': about,'privacy':privacy, 'term':term})





def formu(request):
	path = os.path.join(BASE_DIR, "userData\\")
	with open(path+'access.txt', 'r') as source:
		DISP = (source.read() == "True")
	if not DISP :
		now = datetime.datetime.now()
		second = now.second+6
		minute = now.minute
		if (second > 59):
			second = second-59
			minute = minute +1
		after = now.replace(second=second,minute=minute)
		while(True):
			if(datetime.datetime.now()>after):
				break
	with open(path+'access.txt', 'w') as source:
		source.write("False")
	os.utime("C:\\Users\\ahlaj\Desktop\\cloudOrchestration\\toscaparser\\tosca_template.py", (time.time(),time.time()))
	if len(request.POST) == 0:
		raise Http404("No MyModel matches the given query.")
	date = time.strftime('%d-%m-%y_%H-%M-%S',time.localtime())
	idUser = "1\\"
	path = path + idUser +"{}"+date+".yaml"
	toscaDefinition = request.FILES['toscaDefinition']
	toscaTemplat = request.FILES['toscaTemplate']
	originalToscaDefPath = BASE_DIR + "\\toscaparser\\elements\\TOSCA_definition_1_0.yaml"
	# sauvegarder le tosca definition introduit par le client 
	with open(path.format("toscaDef_"), 'wb+') as destination:
		for chunk in toscaDefinition.chunks():
			destination.write(chunk)
	with open(originalToscaDefPath, 'wb+') as definition:
		for chunk in toscaDefinition.chunks():
			definition.write(chunk)
	# sauvegarder le template tosca introduit par le client 
	with open(path.format("toscaTemplate_"), 'wb+') as destination:
		for chunk in toscaTemplat.chunks():
			destination.write(chunk)
	print (DISP)
	return render(request , 'att.html',{'path': idUser+"toscaTemplate_"+date+".yaml"})




def renv(request):
	path = os.path.join(BASE_DIR, "userData\\")
	with open(path+'access.txt', 'r') as source:
		DISP = (source.read() == "True")
	if not DISP:
		originalToscaDefPath = BASE_DIR + "\\toscaparser\\elements\\TOSCA_definition_1_0.yaml"
		secureToscaDefPath = BASE_DIR + "\\toscaparser\\secure\\TOSCA_definition_1_0.yaml"
		try:
			temp = ToscaTemplate(path+request.POST["path"])
		except:
			# restaurer le tosca definition original
			with open(secureToscaDefPath, 'rb') as definition:
				with open(originalToscaDefPath, 'wb+') as destination:
					destination.write(definition.read())
			with open(path+'access.txt', 'w') as source:
				source.write("True")
			raise Http404("Erreur type node")
		graphe = temp.graph
		nodes = graphe.nodetemplates
		mon_fichier = open(path+request.POST["path"], "r")
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
		with open(secureToscaDefPath, 'rb') as definition:
			with open(originalToscaDefPath, 'wb+') as destination:
				destination.write(definition.read())
		with open(path+'access.txt', 'w') as source:
			source.write("True")
		return render(request , 'graph.html',{'noeuds': noeuds,'relations':rel, 'file':file})
	else:
		raise Http404("Session end.")

