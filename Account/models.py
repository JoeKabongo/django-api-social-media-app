from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserAccount(AbstractUser):
    email = models.EmailField(unique=True) # or skip unique
    bio = models.CharField(max_length = 200, default=" ", blank=True)
    profileImage = models.CharField(max_length=1000, default="https://res.cloudinary.com/dgknrkenk/image/upload/v1579667401/uwjxuqzu4baspaqybrmp.png")
    friends = models.IntegerField(default=0)
    isWriter = models.BooleanField(default=False)

    list_display = ('email', 'bio', 'is_writer')

    def get_profileImage(self):
        return self.profileImage


class UpdatePasswordToken(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="user")
    token = models.CharField(max_length=100)


    