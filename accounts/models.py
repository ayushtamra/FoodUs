from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        'username',
        max_length=50,
        unique=True,
        help_text='Required. 50 characters or fewer. Letters, digits and @/./+/-/_ only.',
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })

    is_customer = models.BooleanField('customer status', default=False)
    is_restaurant_owner = models.BooleanField('restaurant owner status', default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __unicode__(self):
        return self.email

    def __str__(self):
        return self.get_full_name()


class Location(models.Model):
    LocationId = models.AutoField(primary_key=True)
    LocationName = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.LocationName

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    f_name = models.CharField(max_length=20, blank=False)
    l_name = models.CharField(max_length=20, blank=False)
    phone = models.CharField(max_length=10, blank=False)
    addressline1 = models.TextField(max_length=20, blank=False)
    addressline2 = models.TextField(max_length=20, blank=False)

    def __str__(self):
        return self.user.username


class RestaurantOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    f_name = models.CharField(max_length=20, blank=False)
    l_name = models.CharField(max_length=20, blank=False)
    phone = models.CharField(max_length=10, blank=False)
    addressline1 = models.TextField(max_length=20, blank=False)
    addressline2 = models.TextField(max_length=20, blank=False)

    def __str__(self):
        return self.user.username
