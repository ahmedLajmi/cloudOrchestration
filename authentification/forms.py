from django.contrib.auth.models import User  #basic user class
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.core.exceptions import ValidationError
from .models import NodePersonalised

#make a new user form class

#class UserForm(forms.ModelForm): # Model :blueprint to be used when making the forms
	
 	# password = forms.CharField(widget=forms.PasswordInput)

 	# class Meta:  # information about my class
 	# 	model = User  #whenever user sign in it goes to the same class
 	# 	fields = ['username', 'email' , 'password']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input form-control','placeholder': 'Enter your Password'}))
    password2 = forms.CharField(label="Repeat password", 
    	widget=forms.PasswordInput(attrs={'class': 'input form-control','placeholder': 'Confirm your Password'}))
    name = forms.CharField(max_length=30
    	, widget=forms.TextInput(attrs={'class': 'input form-control','placeholder': 'Enter your Name'}) )
    email = forms.EmailField(
    widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Enter your Email'})
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True , 
            	'placeholder': 'Enter your Username' })
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password2'] != cd['password']:
            raise ValidationError("Password don't match")

        return cd['password2']


class NodePForm(forms.ModelForm):
    class Meta:
        model = NodePersonalised
        fields = ['name', 'typen', 'attribute']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': True,
                                               'placeholder': 'Enter node name '}),
            'typen': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': False,
                                           'placeholder': 'Enter node type '}),
            'attribute': forms.TextInput(attrs={'class': 'input form-control', 'autofocus': False,
                                           'placeholder': 'Enter node attribute '})
        }

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
