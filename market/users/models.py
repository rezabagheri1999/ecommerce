from django.conf import settings
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
# In your_project_folder/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    is_profile_complete = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name="project_user_set",
        related_query_name="project_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name="project_user_set",
        related_query_name="project_user",
    )


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    provience = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}'s Profile"



class ContactMessage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,
        null=True,blank=True,verbose_name='کاربر'
    )
    name = models.CharField(max_length=8,verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(max_length=11,blank=True,null=True,verbose_name='شماره')
    subject = models.CharField(max_length=200,verbose_name='موضوع')
    message = models.TextField(verbose_name='پیام')
    created_at = models.DateTimeField(auto_now_add = True,verbose_name='زمان ایجاد پیام')
    is_read= models.BooleanField(default=False,verbose_name='خوانده شده ')



    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'صندوق پیام ها'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.subject} - {self.name}'



















