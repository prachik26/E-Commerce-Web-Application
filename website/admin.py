from django.contrib import admin
from website.models import Customer, Order, OrderItem, ShippingAddress


# Register your models here.
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
