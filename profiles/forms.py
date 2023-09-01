import re
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class Registration(forms.Form):
    
    first_name = forms.CharField(
        max_length=20,
        label='First Name',
        widget=forms.TextInput(
            attrs={
                'class':'w-full bg-gray-800 bg-opacity-40 rounded border border-gray-700 focus:border-green-500 focus:bg-gray-900 focus:ring-2 focus:ring-green-900 text-base outline-none text-gray-100 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
                }        #in attributes enter class and id details for html
        )
    )
    last_name = forms.CharField(
        max_length=20,
        label='Last Name',
        widget=forms.TextInput(
            attrs={
                'class':'w-full bg-gray-800 bg-opacity-40 rounded border border-gray-700 focus:border-green-500 focus:bg-gray-900 focus:ring-2 focus:ring-green-900 text-base outline-none text-gray-100 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            }
        )
    )
    username = forms.CharField(
        max_length=20,
        label='username',
        widget=forms.TextInput(
            attrs={
                'class':'w-full bg-gray-800 bg-opacity-40 rounded border border-gray-700 focus:border-green-500 focus:bg-gray-900 focus:ring-2 focus:ring-green-900 text-base outline-none text-gray-100 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            }
        )
    )
    email = forms.EmailField(
        label = 'Email',
        widget = forms.EmailInput(
            attrs={
                'class':'w-full bg-gray-800 bg-opacity-40 rounded border border-gray-700 focus:border-green-500 focus:bg-gray-900 focus:ring-2 focus:ring-green-900 text-base outline-none text-gray-100 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            }
        )
    )
    password = forms.CharField(
        label='Password',
        widget=forms.TextInput(
            attrs={
                'class':'w-full bg-gray-800 bg-opacity-40 rounded border border-gray-700 focus:border-green-500 focus:bg-gray-900 focus:ring-2 focus:ring-green-900 text-base outline-none text-gray-100 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            }
        )
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'class':'w-full bg-gray-800 bg-opacity-40 rounded border border-gray-700 focus:border-green-500 focus:bg-gray-900 focus:ring-2 focus:ring-green-900 text-base outline-none text-gray-100 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            }
        )
    )
    village= forms.CharField(
        max_length=20,
        label='Village',
        widget=forms.TextInput(
            attrs={
                'class':'w-full bg-gray-800 bg-opacity-40 rounded border border-gray-700 focus:border-green-500 focus:bg-gray-900 focus:ring-2 focus:ring-green-900 text-base outline-none text-gray-100 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            }
        )
    )
    mandal = forms.CharField(
        max_length=20,
        label='Mandal',
        widget=forms.TextInput(
            attrs={
                'class':'w-full bg-gray-800 bg-opacity-40 rounded border border-gray-700 focus:border-green-500 focus:bg-gray-900 focus:ring-2 focus:ring-green-900 text-base outline-none text-gray-100 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            }
        ),
        required=True,
    )
    district = forms.CharField(
        max_length=20,
        label='District',
        widget=forms.TextInput(
            attrs={
                'class':'w-full bg-gray-800 bg-opacity-40 rounded border border-gray-700 focus:border-green-500 focus:bg-gray-900 focus:ring-2 focus:ring-green-900 text-base outline-none text-gray-100 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            }
        ),
        required=True,
    )
    state = forms.CharField(
        max_length=20,
        label='State',
        widget=forms.TextInput(
            attrs={
                'class':'w-full bg-gray-800 bg-opacity-40 rounded border border-gray-700 focus:border-green-500 focus:bg-gray-900 focus:ring-2 focus:ring-green-900 text-base outline-none text-gray-100 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            }
        ),
        required=True,
    )
    country = forms.CharField(
        max_length=20,
        label='Country',
        widget=forms.TextInput(
            attrs={
                'class':'w-full bg-gray-800 bg-opacity-40 rounded border border-gray-700 focus:border-green-500 focus:bg-gray-900 focus:ring-2 focus:ring-green-900 text-base outline-none text-gray-100 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            }
        ),
        required=True,
    )
    pin = forms.CharField(
        max_length=20,
        label='pin',
        widget=forms.TextInput(
            attrs={
                'class':'w-full bg-gray-800 bg-opacity-40 rounded border border-gray-700 focus:border-green-500 focus:bg-gray-900 focus:ring-2 focus:ring-green-900 text-base outline-none text-gray-100 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out',
            }
        ),
        required=True,
    )
    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username__iexact=username)
        
        if qs.exists():
            raise forms.ValidationError("This is an invalid username, please pick another.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = User.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_password2(self):
        pwd = self.cleaned_data.get("password2")
        pw = self.cleaned_data.get("password")
        if pwd != pw:
            raise forms.ValidationError("password doesn't match")

class Loginform(forms.Form):
    username = forms.CharField(
        max_length=50,
        label = 'Username/Email',
        widget = forms.TextInput(
            attrs={
                'class':'form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-green-600 focus:outline-none',
            }
        )
        )
    password = forms.CharField(
        max_length=20,
        label = 'Password',
        widget = forms.PasswordInput(
            attrs={
                'class':'form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-green-600 focus:outline-none',
            }
            
        )
    )

    
    
class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        widget = forms.EmailInput(
            attrs = {
                'class':'form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none',
                'placeholder': 'Enter your registered email address',
            }
        )
    )
