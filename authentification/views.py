from django.shortcuts import render, get_object_or_404 , redirect , render_to_response
from django.views import generic
from django.views.generic.edit import CreateView , UpdateView , DeleteView #when i want to make a form form maj
from django.urls import reverse_lazy
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login
from django.views.generic import View 
from .forms import UserForm , SignUpForm

from django.template.context_processors import csrf
from django.http import Http404 
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import NodePersonalised

from django.http import Http404
from toscaparser.tosca_template import ToscaTemplate
import importlib
import datetime
import os
import time
import sys



# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def home(request):
	return render(request , 'authentification/home.html')

def register(request):
	return render(request , 'authentification/register.html')

def workspace(request):
	return render(request , 'authentification/workspace.html')

	
def graph(request):
	return render(request , 'authentification/graph.html')


class TagType:
    def __init__(self):
        pass
    success, info, warning, danger = range(4)

class Messages:
    def __init__(self,message, tag):
        self.message = message
        if tag == 0:
            self.tag = "alert alert-success"
        elif tag == 1:
            self.tag = "alert alert-info"
        elif tag == 2:
            self.tag = "alert alert-warning"
        else:
            self.tag = "alert alert-danger"






def login(request):

    if request.method == 'POST':
        username = request.POST['u']
        password = request.POST['p']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request=request, user=user)
            return HttpResponseRedirect(reverse('authentification:workspace'))
        else:
            msg_to_html = Messages('Invalid Credentials', TagType.danger)
            dictionary = dict(request=request, messages = msg_to_html)
            dictionary.update(csrf(request))
            return render_to_response('authentification/login.html', dictionary)
    elif request.method == 'GET':
        return render(request, 'authentification/login.html')



class UserFormView(View):
    form_class = UserForm
    template_name = 'authentification/register.html'
    def get(self,request):
        form = self.form_class(None)
        return render(request, self.template_name , {'form': form}) #to display blank form

    def post(self, request):  # if user clicks submit : process from data base
        form = self.form_class(
            request.POST)  # when clicks submit, all info data get stored in POST data to be passed to the form and the form valid the data

        if form.is_valid():  # store the info in data base but first make check validations
            user = form.save(
                commit=False)  # make a user object using whatever typed in the form but does not save it in data base
            # get cleaned (normalized) data : unifier la forme
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # how to set user passwords , because they have h value
            user.set_password(password)
            user.save()  # put user in data base

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:  # compte banned by admin
                    auth_login(request, user)  # log the user in a session
                # now the user is loged in whatever the info i want i put request.user.username..

                # now redirect them to the home page
                return redirect('authentification:workspace')

        return render(request, self.template_name, {'form': form})


# this def is if you want to change the user's password
def update_pwd(username, pwd):
    user_model = User.objects.get(username=username)
    user_model.set_password(pwd)
    user_model.save()










class IndexView(generic.ListView):
	
	template_name = 'authentification/nodeslist.html'  
	context_object_name = 'all_nodes'  
	def get_queryset(setf):  #get objects
		return NodePersonalised.objects.all()


class DetailView(generic.DetailView):
	
	model = NodePersonalised  
	template_name = 'authentification/detailnode.html' 

def detailNode(request, id):
	try:
		node =  NodePersonalised.objects.get(pk=id)
	except NodePersonalised.DoesNotExist:
	 	raise Http404("Node does not exist")

	return render(request,'authentification/detailnode.html', {'node': node}) 


class NodePCreate (CreateView):
	model = NodePersonalised 
	fields = [ 'name' , 'typen' , 'attribute' ,'photo' ]   #what fields i want to fill


class NodePUpdate (UpdateView):
	model = NodePersonalised 
	fields = [ 'name' , 'typen' , 'attribute' ,'photo']   #what fields i want to fill


class NodePDelete (DeleteView):
	model = NodePersonalised  
	success_url =reverse_lazy('authentification:list')





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
	os.utime("C:\\PCD\\GitV3\\cloudOrchestration\\toscaparser\\tosca_template.py", (time.time(),time.time()))
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
	return render(request , 'authentification/att.html',{'path': idUser+"toscaTemplate_"+date+".yaml"})




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
		return render(request , 'authentification/graph.html',{'noeuds': noeuds,'relations':rel, 'file':file})
	else:
		raise Http404("Session end.")

