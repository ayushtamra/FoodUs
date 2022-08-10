from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(RestaurantOwner)
admin.site.register(Location)