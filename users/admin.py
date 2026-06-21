from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(CustomerUser)
class CustomerUserAdmin(admin.ModelAdmin):
    model = CustomerUser
    list_display = ('username','teacher','phone_number')
    list_editable = ('teacher',)
    list_filter = ('teacher',)
    search_fields = ('username','phone_number')