from django.shortcuts import render, get_object_or_404 , redirect , render_to_response
from django.views import generic
from django.views.generic.edit import CreateView , UpdateView , DeleteView #when i want to make a form form maj
from django.urls import reverse_lazy
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login
from django.views.generic import View 
from .forms import UserForm , SignUpForm

from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import NodePersonalised

from django.http import Http404

import os




# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



class Messages:
    success, info, warning, danger = range(4)
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
            return render(request, 'authentification/workspace.html')
        else:
            msg_to_html = Messages('Invalid Credentials', Messages.danger)
            dictionary = dict(request=request, messages = msg_to_html)
            dictionary.update(csrf(request))
            return render_to_response('authentification/login.html', dictionary)
    elif request.method == 'GET':
        if request.user.is_authenticated is False:
            return render(request, 'authentification/login.html')
        else:
            return HttpResponseRedirect(reverse('home'))




class UserFormView(View):
    form_class = UserForm
    template_name = 'authentification/register.html'

    def get(self,request):
        form = self.form_class(None)
        if request.user.is_authenticated is False:
            return render(request, self.template_name, {'form': form})  #to display blank form
        else:
            return HttpResponseRedirect(reverse('home'))


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
                return redirect('home')

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




