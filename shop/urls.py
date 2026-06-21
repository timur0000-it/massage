from django.urls import path,include

from .views import *
app_name = 'shop'
urlpatterns = [
    path('my_cart/', my_cart,name='my_cart'),
    path('create_order/', create_order,name='create_order'),
    path('create_checkout_session/<int:order_id>/', create_checkout_session,name='create_checkout_session'),
    path('stripe/success/<int:order_id>/', stripe_success,name='stripe_success'),
    path('stripe/cancel/<int:order_id>/', stripe_cancel,name='stripe_cancel'),
    path('add_cart/<int:course_id>', add_cart,name='add_cart'),
    path('delete_cart/<int:course_id>', delete_cart,name='delete_cart'),
    path('all_courses/', all_courses, name='all_courses'),
    

]
