# models.py
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    from_signal = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user)
        
        
# buyers>apps.py
from django.apps import AppConfig

class BuyersConfig(AppConfig):
    name = 'buyers'

    def ready (self):
        import buyers.signals

     
# buyers>__init__.py
default_app_config = 'buyers.apps.BuyersConfig


# buyers>signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Buyer

@receiver(post_save, sender=User)
def post_save_create_buyer(sender, instance, created, **kwargs):
    print('sender', sender)
    print('instance', instance)
    print('created', created)
    if created:
        Buyer.objects.create(user=instance)
        
        
        
        
        
        
# cars>models.py
from django.db import models
from buyers.models import Buyer
import uuid

# Create your models here.
class Car(models. Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.name}-{self.price}-{self.buyer}"
    
    # traditionnal method without signal
    def save(self, *args, **kwargs):
        if self.code == "":
            self.code = str(uuid.uuid4()).replace("-", "").upper()[:10]
        return super().save(*args, **kwargs)

# cars>admin.py
from django.contrib import admin
from .models import Car

# Register your models here.
admin.site.register(Car)


# cars>apps.py
from django.apps import AppConfig

class CarsConfig(AppConfig):
    name = 'buyers'

    def ready (self):
        import cars.signals
        

# cars>__init__.py
default_app_config = 'cars.apps.CarsConfig


# cars>signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from buyers.models import Buyer
from .models import Car
import uuid

@receiver(pre_save, sender=Car)
def pre_save_create_code(sender, instance, **kwargs):
    if instance.code == "":
        instance.code = str(uuid.uuid4()).replace("-", "").upper()[:10]
    obj = Buyer.objects.get(user=instance.buyer.user)
    obj.from_signal = True
    obj.save()
    
    
    
**********************************************************************************
**********************************************************************************
**********************************************************************************

# signals.py
from django.contrib.auth.models import User
from djnago.db.models.signals import post_save

# receiver function
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
 
post_save.connect(save_profile, sender=User)

# Or

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


# @receiver([post_save, post_delete], sender=User)


# Files organization using @receiver --------------------------------------------

# profiles/signals.py:
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from cmdbox.profiles.models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
   
# profiles/app.py:
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class ProfilesConfig(AppConfig):
    name = 'cmdbox.profiles'
    verbose_name = _('profiles')

    def ready(self):
        import cmdbox.profiles.signals  # noqa
        
      
# profiles/__init__.py:
default_app_config = 'cmdbox.profiles.apps.ProfilesConfig'



# Files organization without @receiver --------------------------------------------

# profiles/signals.py:
from cmdbox.profiles.models import Profile

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
# profiles/app.py:
from django.apps import AppConfig
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from cmdbox.profiles.signals import create_user_profile, save_user_profile

class ProfilesConfig(AppConfig):
    name = 'cmdbox.profiles'
    verbose_name = _('profiles')

    def ready(self):
        post_save.connect(create_user_profile, sender=User)
        post_save.connect(save_user_profile, sender=User)


# profiles/__init__.py:
default_app_config = 'cmdbox.profiles.apps.ProfilesConfig'


# Signals in Models --------------------------------------------
# models.py *
from django.db import models
from django.db.models.signals import (post_save, pre_save, post_delete)

class Post(models.Model):
    title = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title
        
    def save_post(sender, instance, **kwargs):
        print("something")
        
    def after_delete_post(sender, instance, **kwargs):
        print("you delete something")
    
    post_save.connect(save_post, sender=Post)
    post_delete.connect(after_delete_post, sender=Post)
    
    
 **************************************************************
 **************************************************************
 
 # Define personal signal
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from .post import Post
from django.core.signals import request_finished
from django.shortcuts import render
from django.http import HttpResponse

request_counter_signal = Signal(providing_args=['timestamp'])

def home(request):
    request_counter_signal.send(sender=POST, timestamp='2022 10 10')
    return HttpResponse("Here's the response")
    
@receiver(request_counter_signal)
def post_counter_signal_receiver(sender, **kwargs):
    print(kwargs)
    
    
    
    
    
    
    
    
    
    
    
    
    
********************************************** EXEMPLE ***************************************
**********************************************************************************************

from django.db import models

# Create your models here.

class Officer(models.Model):
    name = models.CharField(max_length=256)
    rank = models.ForeignKey('Rank', on_delete=models.CASCADE)
    ship_assignment = models.ForeignKey('Ship', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Rank(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Ship(models.Model):
    name = models.CharField(max_length=256)
    registry = models.CharField(max_length=256)
    captain = models.OneToOneField('Officer', default=None, on_delete=models.CASCADE, blank=True, null=True)
    ship_class = models.CharField(max_length=256)
    status = models.CharField(max_length=256)

    def __str__(self):
        return self.name
        
        
        
@receiver(post_save, sender=Officer)
def send_new_officer_notification_email(sender, instance, created, **kwargs):

    # if a new officer is created, compose and send the email
    if created:
        name = instance.name if instance.name else "no name given"
        rank = instance.rank.name if instance.rank else "no rank given"
        ship_assignment = instance.ship_assignment.name if instance.ship_assignment else 'no ship assignment'

        subject = 'NAME: {0}, RANK: {1}, SHIP ASSIGNMENT: {2}'.format(name, rank, ship_assignment)
        message = 'A New Officer has been assigned!\n'
        message += 'NAME: ' + name + '\n' + 'RANK: ' \
                  + rank + '\n' + 'SHIP ASSIGNMENT: ' + ship_assignment + '\n'
        message += '--' * 30

        send_mail(
            subject,
            message,
            'your_email@example.com',
            ['recipeint1@xample.com', 'recipent2@xample.com '],
            fail_silently=False,
        )





from django.db import models
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Officer(models.Model):
    name = models.CharField(max_length=256)
    rank = models.ForeignKey('Rank', on_delete=models.CASCADE)
    ship_assignment = models.ForeignKey('Ship', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Rank(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Ship(models.Model):
    name = models.CharField(max_length=256)
    registry = models.CharField(max_length=256)
    captain = models.OneToOneField('Officer', default=None, on_delete=models.CASCADE, blank=True, null=True)
    ship_class = models.CharField(max_length=256)
    status = models.CharField(max_length=256)

    def __str__(self):
        return self.name


@receiver(post_save, sender=Officer)
def send_new_officer_notification_email(sender, instance, created, **kwargs):

    # if a new officer is created, compose and send the email
    if created:
        name = instance.name if instance.name else "no name given"
        rank = instance.rank.name if instance.rank else "no rank given"
        ship_assignment = instance.ship_assignment.name if instance.ship_assignment else 'no ship assignment'

        subject = 'NAME: {0}, RANK: {1}, SHIP ASSIGNMENT: {2}'.format(name, rank, ship_assignment)
        message = 'A New Officer has been assigned!\n'
        message += 'NAME: ' + name + '\n' + 'RANK: ' \
                  + rank + '\n' + 'SHIP ASSIGNMENT: ' + ship_assignment + '\n'
        message += '--' * 30

        send_mail(
            subject,
            message,
            'your_email@example.com',
            ['recipeint1@xample.com', 'recipent2@xample.com '],
            fail_silently=False,
        )