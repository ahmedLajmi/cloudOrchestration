"""cloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf.urls import include, url
from django.urls import path
from . import views

app_name = 'authentification' #creer un namespace

urlpatterns = [
    url(r'^$',views.home, name='index'),
    url(r'^register$',views.UserFormView.as_view(), name='register'),
    url(r'^login$',views.login, name='login'),
    url(r'^workspace$',views.workspace, name='workspace'),
    url(r'^home$',views.home, name='home'),
    url(r'^form$',views.formu, name='formu'),
    url(r'^graph$',views.renv, name='graph'),


    url(r'^list/$',views.IndexView.as_view() , name='list'), 
    url(r'^mynode/(?P<id>[0-9]+)/$',views.detailNode , name='detail'), 

    url(r'^node/add/$',views.NodePCreate.as_view() , name='node-add'),
    url(r'^node/(?P<pk>[0-9]+)/$',views.NodePUpdate.as_view() , name='node-update'),
    url(r'^node/(?P<pk>[0-9]+)/delete/$',views.NodePDelete.as_view() , name='node-delete'),

   
]
