from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomerUser(AbstractUser):
    photo = models.ImageField(
        blank=True,
        null=True,
        help_text="Фото профиля (рекомендуемый размер 400x400)",
        upload_to='user_photos/',default="avatar.svg"
    )

    teacher = models.BooleanField(default=False,verbose_name='Вы хотите иметь возможность создавать курсы?')
    phone_number = models.CharField(max_length=32, blank=False, null=False)

    @property
    def is_teacher(self):
        return self.teacher
    
    def __str__(self):
        return self.username