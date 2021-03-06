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

app_name = 'createTemplate' #creer un namespace


urlpatterns = [

    url(r'^listNode/$', views.list, name='list'),
    url(r'^generateForm/$', views.form, name='templateForm'),
    #url(r'^validateForm/$', views.validateForm, name='validateForm'),
    url(r'^loadDist/$', views.loadDist, name='loadDist'),
    url(r'^validateForm/$', views.formGen, name='formGen'),
    url(r'^validateFormRel/$', views.formRel, name='formRel'),

]

