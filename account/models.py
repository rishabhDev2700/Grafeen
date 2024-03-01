from django.db import models

# Create your models here.
'''Models related to accounts'''
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Manager(BaseUserManager):
    '''Custom user manager to use email field as username field'''
    def create_user(self, email, password, **extra_fields):
        '''Method to create a new user'''
        if not email:
            raise ValueError('Email not present')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        '''Method to create a new superuser'''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Why Superuser is not staff? ")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Why Superuser's is_superuser not True?")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    '''Custom user model for authenticating users'''
    username = None
    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_seller = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = Manager()

    def __str__(self):
        return self.email
