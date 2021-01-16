# from django.db.models import fields
# from django.forms import ModelForm
# from .models import Listing

# class ListingForm(ModelForm):
#     class Meta:
#         model = Listing
#         fields = ['name', 'category', 'image', 'description', 'price', ]

from django import forms
from .models import *

CATEGORY_CHOICES = [
    ('', ''),
    ('Fashion', 'Fashion'),
    ('Toys', 'Toys'),
    ('Electronics', 'Electronics'),
    ('Home', 'Home'),
    ('Food', 'Food'),
    ('ETC', 'etc'),
]

class ListingForm(forms.Form):
    name = forms.CharField(
        label='Item Name',
        max_length=100, 
        widget= forms.TextInput(attrs={'placeholder':'What do you want to list?'}),
    )
    category = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        choices=CATEGORY_CHOICES,
    )
    image = forms.ImageField(required=False,)
    description = forms.CharField(
        label="",        
        widget=forms.Textarea(attrs={'placeholder':'Item Descriptions', "rows":5, "cols":50})
    )
    price = forms.IntegerField(
        label='Starting Bid', 
        widget=forms.NumberInput(attrs={'placeholder':' Your desired starting price here'}),
    )

class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'placeholder':'Username'}),
    )
    email = forms.EmailField(
        max_length=100, 
        widget=forms.EmailInput(attrs={'placeholder':'Email'}),
    )
    password = forms.CharField(
        max_length=100, 
        widget=forms.PasswordInput(attrs={'placeholder':'Password'}),
    )
    confirmation = forms.CharField(
        max_length=100, 
        widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}),
    )
