from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import *


class RestaurantDetailForm(forms.ModelForm):
    # field1 = forms.ModelChoiceField(queryset=Location.objects.all())
    class Meta:
        model = Restaurant
        fields = ('name', 'address', 'avg_cost', 'avg_time', 'phone', 'r_logo', 'location')