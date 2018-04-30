from django.db import models

class Service(models.Model):

	BaseNodes = (('compute', 'Compute'),('database', 'Database'),('dbms', 'DBMS'),
		('softwareComponent', 'Software Component'),('webApplication', 'Web Application'),('webServer', 'WebServer'))
	name = models.CharField(max_length=250)
	temps = models.FloatField(default=1000,verbose_name=u'Response Time')
	cout = models.FloatField(default=100,verbose_name=u'Cost')
	disp = models.FloatField(default=0.99,verbose_name=u'Availability')
	lie = models.CharField(choices=BaseNodes,max_length=250,default="compute",verbose_name=u'For')
	

	def get_absolute_url(self):
		return reverse('nodePerso:list')  #when i create user i give pk and return to this page
														#keyWordargs
	def __str__(self):
		return self.name
