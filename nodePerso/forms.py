from django import forms
from .models import NodePersonalised

#make a new user form class

#class UserForm(forms.ModelForm): # Model :blueprint to be used when making the forms
	
 	# password = forms.CharField(widget=forms.PasswordInput)

 	# class Meta:  # information about my class
 	# 	model = User  #whenever user sign in it goes to the same class
 	# 	fields = ['username', 'email' , 'password']

class NodePForm(forms.ModelForm):

    #my_model=forms.ModelChoiceField(queryset=BaseNode.objects.all(), widget=Select(attrs={'style':'background_color:#F5F8EC'}))


    class Meta:
        model = NodePersonalised
        fields = ['name', 'derivedFrom', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                                'placeholder': 'Enter node name '}),
            'derivedFrom' : forms.Select(choices=NodePersonalised.BaseNodes,attrs={'class':'form-control'})
        }

