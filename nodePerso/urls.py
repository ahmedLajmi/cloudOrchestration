"""cloudOrchestration URL Configuration

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
from django.conf.urls import url
from . import views

app_name = 'nodePerso' #creer un namespace


urlpatterns = [

    url(r'^list/$', views.IndexView.as_view(), name='list'),
    url(r'^details/$', views.detailNode, name='detailNode'),
    url(r'^add/$', views.NodePCreate.as_view(), name='node-add'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.NodePUpdate.as_view(), name='node-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.NodePDelete.as_view(), name='node-delete'),

]

