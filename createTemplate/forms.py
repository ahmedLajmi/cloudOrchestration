from django import forms
from nodePerso.models import NodePersonalised,PersoAttribute
from .models import *
#make a new user form class

#class UserForm(forms.ModelForm): # Model :blueprint to be used when making the forms
	
 	# password = forms.CharField(widget=forms.PasswordInput)

 	# class Meta:  # information about my class
 	# 	model = User  #whenever user sign in it goes to the same class
 	# 	fields = ['username', 'email' , 'password']

class ComputeForm(forms.ModelForm):

  #my_model=forms.ModelChoiceField(queryset=BaseNode.objects.all(), widget=Select(attrs={'style':'background_color:#F5F8EC'}))

  architectureChoices = (("x64","x64"),("x86","x86"))
  os_typeChoices = (("windows","Windows"),("linux","Linux"))
  distributionChoices = (("windowsXp","Windows Xp"),("windows7","Windows 7"),("windows10","Windows 10"),("ubuntu","Ubuntu"),("mint","Mint"))



  architecture = forms.ChoiceField(choices=architectureChoices, widget=forms.Select(attrs={'class':'form-control'}))
  os_type = forms.ChoiceField(choices=os_typeChoices, widget=forms.Select(attrs={'onchange':'loadDist();','id':'os_type' ,'class':'form-control'}))
  distribution = forms.ChoiceField(choices=distributionChoices,widget=forms.Select(attrs={'class':'form-control','id':'distribution'}))
  class Meta:
      model = Compute
      fields = ['name','num_cpus', 'disk_size', 'mem_size', 'architecture', 'os_type', 'distribution', 'version']
      fieldsets = (
            ('Host', {
                'fields': ('num_cpus', 'disk_size','mem_size'),
            }),
            ("Operating system", {
                'fields': ('architecture', 'os_type','distribution','version'),
            }),
        )
      widgets = {
          'name': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''}),
         'num_cpus': forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''}),
         'disk_size': forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''}),
         'mem_size': forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''}),
         'version': forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''})
      }
      
  def __init__(self, *args, **kwargs):
    if 'persoNode' in kwargs:
      self.persoNode = kwargs.pop('persoNode', None)
      super(ComputeForm, self).__init__(*args, **kwargs)
      for attribute in self.persoNode.persoattribute_set.all():
        if attribute.type == "text":
          self.fields[attribute.name] = forms.CharField(widget=forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''}))
        else:
          self.fields[attribute.name] = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''}))
    else:
      super(ComputeForm, self).__init__(*args, **kwargs)


class DatabaseForm(forms.ModelForm):
  class Meta:
      model = Database
      fields = ['nameInst','name', 'user', 'password', 'port']
      widgets = {
         'nameInst': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''}),
         'name': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''}),
         'user': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''}),
         'password': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''}),
         'port': forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''})
      }
  def __init__(self, *args, **kwargs):
    if 'persoNode' in kwargs:
      self.persoNode = kwargs.pop('persoNode', None)
      super(DatabaseForm, self).__init__(*args, **kwargs)
      for attribute in self.persoNode.persoattribute_set.all():
        if attribute.type == "text":
          self.fields[attribute.name] = forms.CharField(widget=forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''}))
        else:
          self.fields[attribute.name] = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''}))
    else:
      super(DatabaseForm, self).__init__(*args, **kwargs)

  
class DbmsForm(forms.ModelForm):

  class Meta:
      model = Dbms
      fields = ['name','root_password', 'port']
      widgets = {
          'name': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''}),
         'root_password': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''}),
         'port': forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''})
      }
  def __init__(self, *args, **kwargs):
    if 'persoNode' in kwargs:
      self.persoNode = kwargs.pop('persoNode', None)
      super(DbmsForm, self).__init__(*args, **kwargs)
      for attribute in self.persoNode.persoattribute_set.all():
        if attribute.type == "text":
          self.fields[attribute.name] = forms.CharField(widget=forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''}))
        else:
          self.fields[attribute.name] = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''}))
    else:
      super(DbmsForm, self).__init__(*args, **kwargs)


class SoftwareComponentForm(forms.ModelForm):

  class Meta:
      model = SoftwareComponent
      fields = ['name','component_version']
      widgets = {
          'name': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''}),
         'component_version': forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''})
      }
  def __init__(self, *args, **kwargs):
    if 'persoNode' in kwargs:
      self.persoNode = kwargs.pop('persoNode', None)
      super(SoftwareComponentForm, self).__init__(*args, **kwargs)
      for attribute in self.persoNode.persoattribute_set.all():
        if attribute.type == "text":
          self.fields[attribute.name] = forms.CharField(widget=forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''}))
        else:
          self.fields[attribute.name] = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''}))
    else:
      super(SoftwareComponentForm, self).__init__(*args, **kwargs)


class WebApplicationForm(forms.ModelForm):

  class Meta:
      model = WebApplication
      fields = ['name','context_root']
      widgets = {
          'name': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''}),
         'context_root': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''}),
      }
  def __init__(self, *args, **kwargs):
    if 'persoNode' in kwargs:
      self.persoNode = kwargs.pop('persoNode', None)
      super(WebApplicationForm, self).__init__(*args, **kwargs)
      for attribute in self.persoNode.persoattribute_set.all():
        if attribute.type == "text":
          self.fields[attribute.name] = forms.CharField(widget=forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''}))
        else:
          self.fields[attribute.name] = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''}))
    else:
      super(WebApplicationForm, self).__init__(*args, **kwargs)


class WebServerForm(forms.ModelForm):

  class Meta:
      model = WebServer
      fields = ['name','component_version']
      widgets = {
          'name': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''}),
         'component_version': forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                             'placeholder': ''})
      }
  def __init__(self, *args, **kwargs):
    if 'persoNode' in kwargs:
      self.persoNode = kwargs.pop('persoNode', None)
      super(WebServerForm, self).__init__(*args, **kwargs)
      for attribute in self.persoNode.persoattribute_set.all():
        if attribute.type == "text":
          self.fields[attribute.name] = forms.CharField(widget=forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''}))
        else:
          self.fields[attribute.name] = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''}))
    else:
      super(WebServerForm, self).__init__(*args, **kwargs)


"""class NodePForm(forms.ModelForm):
 'name': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': 'Enter node name '}),
            'derivedFrom' : forms.Select(attrs={'class':'form-control'})

    #my_model=forms.ModelChoiceField(queryset=BaseNode.objects.all(), widget=Select(attrs={'style':'background_color:#F5F8EC'}))



    class Meta:
        model = NodePersonalised
        fields = ['name', 'derivedFrom', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': 'Enter node name '}),
            'derivedFrom' : forms.Select(attrs={'class':'form-control'})
        }"""

