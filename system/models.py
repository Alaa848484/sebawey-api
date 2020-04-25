
from datetime import datetime
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)



# Should exist in every model 
class BaseModel(models.Model):
    class Meta:
        abstract = True
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =  models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True , blank=True)
    is_deleted =  models.BooleanField(default=False)
    uuid = models.UUIDField(default=uuid.uuid4 , editable=False, unique=True)
    
    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.is_deleted = True    
        self.save()
        



class StudentProfile(models.Model):
    user = models.OneToOneField(User, verbose_name="TheUser", on_delete=models.CASCADE , primary_key=True)
    full_name = models.CharField(max_length=100)
    birth_date = models.IntegerField(verbose_name="Student Age" , null=True )
    location = models.CharField(max_length=30 , blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

