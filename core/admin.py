from django.contrib import admin
from .models import Restaurant, FoodItem, FoodRestaurant, Offer, Order, OrderDetail, \
    Favourite, ItemType, Payment, Cuisine


admin.site.register(Restaurant)
admin.site.register(ItemType)
admin.site.register(FoodRestaurant)
admin.site.register(FoodItem)
admin.site.register(OrderDetail)
admin.site.register(Order)
admin.site.register(Offer)
admin.site.register(Favourite)
admin.site.register(Cuisine)
admin.site.register(Payment)
