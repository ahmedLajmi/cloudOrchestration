from django.db import models

class Compute(models.Model):

    num_cpus = models.IntegerField(verbose_name=u'Number of CPUs')
    disk_size = models.IntegerField(verbose_name=u'Disk size (GB)')
    mem_size = models.IntegerField(verbose_name=u'Memory size (MB)')
    architecture = models.CharField(max_length = 250)
    os_type = models.CharField(max_length = 250,verbose_name=u'OS type')
    distribution = models.CharField(max_length = 250)
    version = models.FloatField(max_length=3)
    name = models.CharField(max_length = 250,verbose_name=u'Instance name')

    def definition(self,perso = None):
    	definition= ''' 
    '''+self.name+''':'''
    	if (perso == None):
    		definition +='''
      type: tosca.nodes.Compute'''
    	else:
    		definition += '''
      type: '''+perso
    	definition +='''
      capabilities: '''		
    	if (self.num_cpus is not None or self.disk_size is not None or self.mem_size is not None ):
    		definition += '''
        host:
          properties:'''
    		if self.num_cpus is not None:
    			definition += ''' 
            num_cpus: '''+str(self.num_cpus)
    		if self.disk_size is not None:
    			definition += '''
            disk_size: '''+str(self.disk_size) + ''' GB'''
    		if self.mem_size is not None:
    			definition += '''
            mem_size: '''+str(self.mem_size) + ''' MB'''

    	if (self.architecture is not None or self.os_type is not None or self.distribution is not None or self.version is not None ):
    		definition += '''
        os:
          properties: '''
    		if self.architecture is not None:
    			definition += '''
            architecture: '''+str(self.architecture)
    		if self.os_type is not None:
    			definition += '''
            type: '''+str(self.os_type)
    		if self.distribution is not None:
    			definition += '''
            distribution: '''+str(self.distribution)
    		if self.version is not None:
    			definition += '''
            version: '''+str(self.version)

    	return definition


class Database(models.Model):

	name = models.CharField(max_length = 250)
	user = models.CharField(max_length = 250)
	password = models.CharField(max_length = 250)
	port = models.IntegerField()
	nameInst = models.CharField(max_length = 250,verbose_name=u'Instance name')
	def definition(self,perso = None):
		definition = '''
    '''+self.nameInst+''':'''
		if (perso == None):
			definition +='''
      type: tosca.nodes.Database'''
		else:
			definition += '''
      type: '''+perso
		if(self.name is not None or self.user is not None or self.password is not None or self.port is not None):
			definition += '''
      properties:'''
			if (self.name is not None):
				definition += '''
        name: '''+str(self.name)
			if (self.user is not None):
				definition += '''
        user: '''+str(self.user)
			if (self.password is not None):
				definition += '''
        password: '''+str(self.password)
			if (self.port is not None):
				definition += '''
        port: '''+str(self.port)
		return definition
	def host(self,host):
		relation = '''
      requirements:
        - host: '''+host
		return relation

class Dbms(models.Model):

	root_password = models.CharField(max_length = 250)
	port = models.IntegerField()
	name = models.CharField(max_length = 250,verbose_name=u'Instance name')

	def definition(self,perso = None):
		definition = '''
    '''+self.name+''':'''
		if (perso == None):
			definition +='''
      type: tosca.nodes.DBMS'''
		else:
			definition += '''
      type: '''+perso
		if(self.root_password is not None or self.port is not None):
			definition += '''
      properties:'''
			if (self.root_password is not None):
				definition += '''
        root_password: '''+str(self.root_password)
			if (self.port is not None):
				definition += '''
        port: '''+str(self.port)
		return definition

	def host(self,host):
		relation = '''
      requirements:
        - host: '''+host
		return relation

    
class SoftwareComponent(models.Model):

	component_version = models.FloatField(max_length = 2)
	name = models.CharField(max_length = 250,verbose_name=u'Instance name')
	def definition(self,perso = None):
		definition = '''
    '''+self.name+''':'''
		if (perso == None):
			definition +='''
      type: tosca.nodes.SoftwareComponent'''
		else:
			definition += '''
      type: '''+perso
		if(self.component_version is not None):
			definition += '''
      properties:'''
			if (self.component_version is not None):
				definition += '''
        component_version: '''+str(self.component_version)
		return definition

	def host(self,host):
		relation = '''
      requirements:
        - host: '''+host
		return relation
	def connectTo(self,connect):
		relation = '''
        - database_endpoint:
            node: ''' + connect +'''
            relationship: tosca.relationships.ConnectsTo'''
		return relation

class WebApplication(models.Model): 

	context_root = models.CharField(max_length = 250)
	name = models.CharField(max_length = 250,verbose_name=u'Instance name')
	def definition(self,perso = None):
		definition = '''
    '''+self.name+''':'''
		if (perso == None):
			definition +='''
      type: tosca.nodes.WebApplication'''
		else:
			definition += '''
      type: '''+perso
		if(self.context_root is not None):
			definition += '''
      properties:'''
			if (self.context_root is not None):
				definition += '''
        context_root: '''+str(self.context_root)
		return definition

	def host(self,host):
		relation = '''
      requirements:
        - host: '''+host
		return relation

	def connectTo(self,connect):
		relation = '''
        - database_endpoint:
            node: ''' + connect +'''
            relationship: tosca.relationships.ConnectsTo'''
		return relation

class WebServer(models.Model):

	component_version = models.FloatField(max_length = 2)
	name = models.CharField(max_length = 250,verbose_name=u'Instance name')
	def definition(self,perso = None):
		definition = '''
    '''+self.name+''':'''
		if (perso == None):
			definition +='''
      type: tosca.nodes.WebServer'''
		else:
			definition += '''
      type: '''+perso
		if(self.component_version is not None):
			definition += '''
      properties:
        component_version: '''+str(self.component_version)
		return definition

	def host(self,host):
		relation = '''
      requirements:
        - host: '''+host
		return relation

class Template(models.Model):

	path = models.CharField(max_length = 250)
	name = models.CharField(max_length = 250)


