from django.contrib import admin
from django.urls import path

from .views import *

app_name = 'accounts'

urlpatterns = [
    path('register/customer/', CustRegisterView.as_view(), name='customer_register'),
    path('login/customer/', CustLoginView.as_view(), name='customer_login'),
    path('register/restaurant/', RestRegisterView.as_view(), name='restaurant_register'),
    path('login/restaurant/', RestLoginView.as_view(), name='restaurant_login'),
    path('logout', LogoutView.as_view(), name='logout'),
]