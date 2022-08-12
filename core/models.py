from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from accounts.models import *



class Offer(models.Model):
    offer_id = models.AutoField(primary_key=True)
    discount = models.IntegerField(blank=False)


class Cuisine(models.Model):
    cuisine_id = models.AutoField(primary_key=True)
    cuisine_name = models.CharField(max_length=20, blank=False)


class Restaurant(models.Model):
    restaurant_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, blank=False)
    owner = models.ForeignKey(RestaurantOwner, on_delete=models.CASCADE)
    address = models.CharField(max_length=50, blank=False)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    avg_time = models.CharField(max_length=4, blank=False)
    avg_cost = models.CharField(max_length=5, blank=False)
    is_exclusive = models.BooleanField(default=False)
    phone = models.CharField(max_length=10, blank=False)
    cuisine = models.ForeignKey(Cuisine, on_delete=models.DO_NOTHING)
    r_logo = models.FileField(blank=True)
    offer = models.ForeignKey(Offer, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class Favourite(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


class ItemType(models.Model):
    type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, blank=False)


class FoodItem(models.Model):
    food_item_id = models.AutoField(primary_key=True)
    type = models.ForeignKey(ItemType, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=40, blank=False)
    is_veg = models.BooleanField(default=True)


class FoodRestaurant(models.Model):
    food_item_id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    cost = models.IntegerField(blank=False)


class Payment(models.Model):
    hash = models.AutoField(primary_key=True)
    amount = models.IntegerField(blank=False)
    datetime = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    offer = models.ForeignKey(Offer, on_delete=models.DO_NOTHING, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    payment_hash = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    instructions = models.TextField(blank=True)
    payment_mode_online = models.BooleanField(default=True)
    tax = models.IntegerField(blank=False)
    rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    review = models.TextField(max_length=250, default='')
    ORDER_STATE_WAITING = "Waiting"
    ORDER_STATE_PLACED = "Placed"
    ORDER_STATE_ACKNOWLEDGED = "Acknowledged"
    ORDER_STATE_COMPLETED = "Completed"
    ORDER_STATE_CANCELLED = "Cancelled"
    ORDER_STATE_DISPATCHED = "Dispatched"

    ORDER_STATE_CHOICES = (
        (ORDER_STATE_PLACED, ORDER_STATE_PLACED),
        (ORDER_STATE_ACKNOWLEDGED, ORDER_STATE_ACKNOWLEDGED),
        (ORDER_STATE_COMPLETED, ORDER_STATE_COMPLETED),
        (ORDER_STATE_CANCELLED, ORDER_STATE_CANCELLED),
        (ORDER_STATE_DISPATCHED, ORDER_STATE_DISPATCHED)
    )
    status = models.CharField(max_length=50, choices=ORDER_STATE_CHOICES, default=ORDER_STATE_PLACED)

    def __str__(self):
        g = str(self.order_id) + " " + self.status
        return str(g)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False, default=1)

    class Meta:
        unique_together = (('food_item', 'order'),)
