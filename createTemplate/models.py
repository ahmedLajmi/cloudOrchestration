from django.db import models

class Compute(models.Model):

    num_cpus = models.IntegerField()
    disk_size = models.IntegerField()
    mem_size = models.IntegerField()
    architecture = models.CharField(max_length = 250)
    os_type = models.CharField(max_length = 250)
    distribution = models.CharField(max_length = 250)
    version = models.FloatField(max_length=3)


class Database(models.Model):

	name = models.CharField(max_length = 250)
	user = models.CharField(max_length = 250)
	password = models.CharField(max_length = 250)
	port = models.IntegerField()

class Dbms(models.Model):

	root_password = models.CharField(max_length = 250)
	port = models.IntegerField()
    
class SoftwareComponent(models.Model):

	component_version = models.FloatField(max_length = 2)

class WebApplication(models.Model): 

	context_root = models.CharField(max_length = 250)

class WebServer(models.Model):

	component_version = models.FloatField(max_length = 2)

