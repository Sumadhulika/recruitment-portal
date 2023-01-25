from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True,default=None)
    username=models.CharField(max_length=50,default=None,unique=True)
    first_name = models.CharField(max_length=30,default='Default', null=False)
    last_name = models.CharField(max_length=30,default='Default', null=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    contact = models.CharField(max_length=15,default='Default', null=False)
    role = models.CharField(max_length=20,default='Default', null=False)
    accesslable = models.IntegerField(default=0, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()


    def save_model(self, request, obj, form, change):
        
        obj.save()




class qualifications(models.Model):

    qualifications=models.CharField(max_length=100,primary_key=True)

    def __str__(self):
         
         return self.qualifications



class skills(models.Model):

    skills=models.CharField(max_length=100,primary_key=True)

    def __str__(self):
         
         return self.skills



class CandidateDetails(models.Model):
    first_name=models.CharField(max_length=45)
    last_name=models.CharField(max_length=45)
    email=models.EmailField(unique=True)
    qualifications=models.ForeignKey(qualifications,on_delete=models.CASCADE)
    skills = models.ManyToManyField(skills)    
    experience=models.IntegerField()
    contact=models.CharField(max_length=10)
    address=models.CharField(max_length=100)
    date=models.DateField(null=True)
    resume=models.FileField(upload_to='resume',null=True)





