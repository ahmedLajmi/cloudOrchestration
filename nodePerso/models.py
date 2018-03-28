from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from datetime import date





class NodePersonalised(models.Model):
	BASE_NODE_TYPE = (
		('compute','Compute'),
		('softwareComponent','Software Component'),
		('webApplication','Web Application'))
	name = models.CharField(max_length=250)
	type = models.CharField(max_length=250,choices= BASE_NODE_TYPE)
	date = models.DateField(("Date"), default=date.today)
	photo = models.FileField(default="img/serveur.jpg")
	user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)


	def get_absolute_url(self):
		return reverse('nodePerso:list')  #when i create user i give pk and return to this page
														#keyWordargs
	def __str__(self):
		return self.name + ' - password: ' + self.type


class PersoAttribute(models.Model):

	type = models.CharField(max_length=250,default="text")
	name = models.CharField(max_length=250)
	value = models.CharField(max_length=250)
	node = models.ForeignKey(NodePersonalised, on_delete=models.CASCADE)