from django.db import models
from django.urls import reverse  
from datetime import date
from django.contrib.auth.models import Permission, User


class NodePersonalised(models.Model):
	name = models.CharField(max_length=250)
	typen = models.CharField(max_length=250)
	attribute = models.CharField(max_length=250)
	date = models.DateField(("Date"), default=date.today)
	photo = models.FileField(default='{% static "img/serveur.jpg" %}')
	user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

	def get_absolute_url(self):  
		return reverse('authentification:detail', kwargs={'id': self.pk})  #when i create user i give pk and return to this page
														#keyWordargs
	def __str__(self):
		return self.name + ' - password: ' + self.typen
