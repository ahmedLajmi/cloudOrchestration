from django import forms
from .models import NodePersonalised

#make a new user form class

#class UserForm(forms.ModelForm): # Model :blueprint to be used when making the forms
	
 	# password = forms.CharField(widget=forms.PasswordInput)

 	# class Meta:  # information about my class
 	# 	model = User  #whenever user sign in it goes to the same class
 	# 	fields = ['username', 'email' , 'password']

class NodePForm(forms.ModelForm):
    type = forms.ChoiceField(widget= forms.Select(attrs={'class': 'form-control'}),choices=NodePersonalised.BASE_NODE_TYPE, label="Type")

    class Meta:
        model = NodePersonalised
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': 'Enter node name '}),
        }

