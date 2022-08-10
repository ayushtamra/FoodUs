from django.contrib import admin
from django.urls import path

from .views import *

app_name = 'core'

urlpatterns = [
    path('', index, name="index"),
    
    path('restaurant/detail', views.restaurant_detail, name='restaurant_detail'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('restaurants/', views.restaurant_index, name='restaurant_index'),
    path('myorders/', views.myorders, name='myorders'),
    path('restaurant/profile', views.restaurantProfile, name='rest_profile'),
    path('restaurant/menu/', views.menu_manipulation, name='menu'),
    path('restaurant/orderlist/', views.orderlist, name='orderlist'),
    path('restaurant/<int:pk>/', views.restuarantMenu, name='menu'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/pay', views.pay, name='pay'),
]