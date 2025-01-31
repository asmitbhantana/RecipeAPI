import uuid
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,\
    PermissionsMixin
from django.conf import settings
# Create your models here.
def recipe_image_file_path(instance,filename):
    '''Generate the file path for new recipe image'''
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/recipe/',filename)

class UserManager(BaseUserManager):

    def create_user(self,email,password=None,**extra_fileds):
        ''''create and saves a new user'''
        if not email:
            raise ValueError('Email not provided')
        user=self.model(email=self.normalize_email(email),**extra_fileds)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,password):
        ''''creates and save a new super user'''
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser=True 
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''' Custom user models supports using email instead of username'''
    email=models.EmailField(max_length=25,unique=True)
    name=models.CharField(max_length=255)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'


class Tag(models.Model):
    '''Tag field for a recipe'''
    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    '''intgredient to be used in a recipe'''
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    '''Recipe model'''
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    time_minutes  = models.IntegerField()
    price = models.DecimalField(max_digits=5,decimal_places=2)
    link = models.CharField(max_length=255,blank=True)
    image = models.ImageField(null=True,upload_to=recipe_image_file_path)
    """django have the features of providing the name of the field in the quotes
    that is mapped in to the model as required"""
    ingredients=models.ManyToManyField('Ingredient')
    tags=models.ManyToManyField('Tag')

    def __str__(self):
        return self.title


