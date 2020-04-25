from __future__ import unicode_literals
from django.core.mail import send_mail
import uuid
from datetime import datetime

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class User(AbstractBaseUser , PermissionsMixin):
    email =  models.EmailField(_('email address') , unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


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
