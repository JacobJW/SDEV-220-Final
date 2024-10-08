from django.db import models
from django import setup
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "finalstore.settings"
setup()

# Create your models here.
class Location(models.Model):
    loc_id = models.AutoField(primary_key=True)
    loc_address = models.CharField(max_length=200,null=True) # the location address

    def __str__(self):
        return self.loc_address

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_first = models.CharField(max_length=50,null=True) # first name
    user_last = models.CharField(max_length=100,null=True) # last name
    card_balance = models.FloatField(null=True) # tracks user's cash balance to spend
    user_points = models.IntegerField(null=True) # tracks users store credit points

    def __str__(self):
        return self.user_last + ", " + self.user_first
    
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=150,null=False) # readable display name
    price = models.FloatField(null=True) # the standard cost of this item
    category = models.CharField(null=True,max_length=50) # product type. ie. coffees, teas, bakery, etc

    def __str__(self):
        return self.product_name + ', $' + str(self.price)

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE) # who placed the order
    loc_id = models.ForeignKey(Location,on_delete=models.CASCADE) # where the order is placed
    order_date = models.DateTimeField(null=True) # time when the order was submitted
    item_total = models.FloatField(null=True,blank=True) # combined cost of all items
    tax = models.FloatField(null=True,blank=True) # additional tax cost, assuming an 8% sales tax rate
    tip = models.FloatField(null=True,blank=True) # additional tip cost, if applicable
    final_total = models.FloatField(null=True,blank=True) # final price once tax and tip are factored in

    def __str__(self):
        return str(self.order_id) + '-' + str(self.order_date)
    
class OrderItem(models.Model):
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE) # which order this item belongs to
    item_no = models.IntegerField(null=True) # item number, relative to order
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE) # product ordered
    quantity = models.IntegerField(null=True) # count of this same item in the order

    def __str__(self):
        return 'Order:' + str(self.order_id) + ', Item:' + str(self.item_no)