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

from django.conf.urls import url
from . import views

app_name = 'authentification' #creer un namespace

urlpatterns = [

    url(r'^register$',views.UserFormView.as_view(), name='register'),
    url(r'^login$',views.login, name='login'),

    url(r'^users/$',views.IndexView.as_view() , name='users'), #im using a class but treat it as view
    url(r'^(?P<pk>[0-9]+)/$',views.DetailView.as_view() , name='detail'), #pk for primary key because detal expects id
    url(r'^add/$', views.userCreate.as_view(), name='user-add'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.userUpdate.as_view(), name='user-update'),
    url(r'^(?P<pk>[0-9]+)/delete/$', views.userDelete.as_view(), name='user-delete'),

]
