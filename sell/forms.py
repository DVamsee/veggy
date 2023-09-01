from django import forms
from django.contrib.auth import get_user_model
from jsonschema import ValidationError
from .models import Products

User = get_user_model()


class verify_mobile_number(forms.Form):
    mobile = forms.IntegerField(
        widget=forms.NumberInput()
    )
    
    def clean_mobile(self):
        num = self.cleaned_data.get('mobile')
        if len(str(num)) == 10:
            return num
        else:
            raise forms.ValidationError('invalid mobile number')
        
# adding product form
class Add_product(forms.Form):
    product_name = forms.CharField(
        label = 'Product Name',
        widget = forms.TextInput(
            attrs={
                'id':'product_name',
                'onchange':"updateName()",
                'class':'form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-green-600 focus:outline-none',
            }
        )
    )
    description = forms.CharField(
        label = 'description',
        widget = forms.TextInput(
        attrs={
            'class':'form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-green-600 focus:outline-none',
        }
        )
    )
    total_quantity = forms.IntegerField(
        label = 'Quantity Available',
        widget = forms.TextInput(
        attrs={
            'class':'form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-green-600 focus:outline-none',
        }
        )
    )
    price = forms.IntegerField(
        label = 'Price',
        widget = forms.TextInput(
        attrs={
            'class':'form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-green-600 focus:outline-none',
        }
        )
    )
    product_image = forms.FileField(
        label = 'upload the product image',
        widget = forms.FileInput(
            attrs={
                'class':"form-control block w-full px-3 py-1.5 text-base font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none",
            }
        )
    )
    
    def clean_product_image(self):
        image = self.cleaned_data.get('product_image')
        if image is None:
            return ValidationError('image error')
    

    
    
    
    