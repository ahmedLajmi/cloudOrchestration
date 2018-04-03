from django import forms

from .models import Compute,Database
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

    architecture = forms.ChoiceField(choices=architectureChoices, widget=forms.Select(attrs={'class':'form-control'}))
    os_type = forms.ChoiceField(choices=os_typeChoices, widget=forms.Select(attrs={'onchange':'loadDist();','id':'os_type' ,'class':'form-control'}))
    distribution = forms.ChoiceField(choices=(), widget=forms.Select(attrs={'class':'form-control','id':'distribution'}))

    class Meta:
        model = Compute
        fields = ['num_cpus', 'disk_size', 'mem_size', 'architecture', 'os_type', 'distribution', 'version']
        widgets = {
           'num_cpus': forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''}),
           'disk_size': forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''}),
           'mem_size': forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''}),
           'version': forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''})

        }

class DatabaseForm(forms.ModelForm):

    class Meta:
        model = Database
        fields = ['name', 'user', 'password', 'port']
        widgets = {
           'name': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''}),
           'user': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''}),
           'password': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''}),
           'port': forms.NumberInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': ''})

        }

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

