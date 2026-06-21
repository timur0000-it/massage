from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display=('user','course')
    search_fields = ('user',)
    list_editable = ('course',)
    list_display_links = ('user',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
