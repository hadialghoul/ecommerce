from django.contrib import admin
from payment.models import ShippingAddress
from payment.models import Order,OrderItem

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
