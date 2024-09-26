from django.contrib import admin
from storeapp.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Location)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)