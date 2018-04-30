from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from datetime import date
from createTemplate.models import *
"""
class BaseNode(models.Model):

	name = models.CharField(max_length=250)
	type = models.CharField(max_length=250)
	date = models.DateField(("Date"), default=date.today)

	def __str__(self):
		return self.name
"""



class NodePersonalised(models.Model):

	BaseNodes = (('compute', 'Compute'),('database', 'Database'),('dbms', 'DBMS'),
		('softwareComponent', 'Software Component'),('webApplication', 'Web Application'),('webServer', 'Web Server'))
	name = models.CharField(max_length=250)
	date = models.DateField(("Date"), default=date.today)
	photo = models.FileField(default="img/serveur.jpg")
	derivedFrom = models.CharField(choices=BaseNodes,max_length=250,default="compute",verbose_name=u'Derived From')
	user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
	

	def get_absolute_url(self):
		return reverse('nodePerso:list')  #when i create user i give pk and return to this page
														#keyWordargs
	def __str__(self):
		return self.name

	def definition(self):
		derived =""
		if self.derivedFrom == "compute":
			derived = "tosca.nodes.Compute"
		elif self.derivedFrom == "database":
			derived = "tosca.nodes.Database"
		elif self.derivedFrom == "dbms":
			derived = "tosca.nodes.DBMS"
		elif self.derivedFrom == "softwareComponent":
			derived = "tosca.nodes.SoftwarComponent"
		elif self.derivedFrom == "webApplication":
			derived = "tosca.nodes.WebApplication"
		elif self.derivedFrom == "webServer":
			derived = "tosca.nodes.WebServer"

		definition = '''
  '''+self.name+''':
    derived_from: '''+derived

		if len(self.persoattribute_set.all())>0:
			definition += '''
    properties:'''
		typep= ''
		for perso in self.persoattribute_set.all():
			if perso.type == 'text':
				typep = 'string'
			else:
				typep = 'integer'
			definition += '''
      '''+perso.name+''':
        type: '''+typep
		return definition




class PersoAttribute(models.Model):

	type = models.CharField(max_length=250,default="text")
	name = models.CharField(max_length=250)
	node = models.ForeignKey(NodePersonalised, on_delete=models.CASCADE)

class PersoAttributeValue(models.Model):

	value = models.CharField(max_length=250)
	persoAtt = models.ForeignKey(PersoAttribute, on_delete=models.CASCADE)
	template = models.ForeignKey(Template, on_delete=models.CASCADE)

	def definition(self):
		definition = '''
        '''+self.persoAtt.name+''': '''+str(self.value)
		return definition