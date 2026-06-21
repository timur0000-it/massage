from django.urls import path, include
from .views import *

app_name = 'users'
urlpatterns = [
    path('signup/', loginPage, name='signup'),
    path('', home, name='home'),
    path('register/', registerPage, name='register'),
    path('user_page/', user_page,name='user_page'),
    path('send_email/<int:course_id>', send_email, name='send_email'),
    path('signout/', signout, name='signout')
]