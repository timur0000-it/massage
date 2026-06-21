from django.db import models
from users.models import *
from courses.models import *
# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(CustomerUser,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="cart_courses")
    
    def total_price(self):
        return self.course.price 
    
    def __str__(self):
        return f'{self.user.username} - {self.course.title} '

    
class Order(models.Model):
    STATUS_CHOISES = (
        ('created','Создан'),
        ('paid','Оплачен'),
        ('canceled','Отменен')
    )
    user =  models.ForeignKey(CustomerUser,on_delete=models.CASCADE)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12,decimal_places=2)
    stripe_id = models.CharField(max_length=250,blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOISES,default='created')