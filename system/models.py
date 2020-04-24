
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)



class Student(models.Model):
    user = models.OneToOneField(User, verbose_name="TheUser", on_delete=models.CASCADE , primary_key=True)
    full_name = models.CharField(max_length=100)
    age = models.IntegerField(verbose_name="Student Age" , null=True )
    