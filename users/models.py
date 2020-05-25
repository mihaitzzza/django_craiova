from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from activation.signals import set_inactive_user


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, is_social_user=False):
        if not email:
            raise ValueError('User must have an e-mail address.')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        if not is_social_user:
            set_inactive_user.send(sender=settings.AUTH_USER_MODEL, user=user)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name):
        user = self.create_user(email, first_name, last_name)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class MyUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, null=False, max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_images/')
    # avatar = models.CharField(max_length=255, null=True)
