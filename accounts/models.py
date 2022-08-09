from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    first_name = None
    last_name = None

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=30)
    discriminator = models.CharField(max_length=5, null=True, blank=True)

    class Meta:
        db_table = 'profile'

    def __str__(self):
        return ''

    # def save(self, *args, **kwargs):
    #     self.provider = SocialAccount.provider
    #     super().save(*args, **kwargs)

    @receiver(user_signed_up)
    def populate_profile(sociallogin, user, **kwargs):

        user.profile = Profile()
        user.profile.provider = sociallogin.account.provider

        if sociallogin.account.provider == 'discord':
            user_data = user.socialaccount_set.filter(provider='discord')[0].extra_data
            discriminator = user_data['discriminator']
        else:
            discriminator = None

        user.profile.discriminator = discriminator
        user.profile.save()
