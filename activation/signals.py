from secrets import token_hex
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import Signal
from activation.models import Activation
from activation.helpers.utils import send_activation_email


def inactivate_user(user, *args, **kwargs):
    if not user.pk:
        user.is_active = False
        pass


set_inactive_user = Signal(providing_args=['user'])
set_inactive_user.connect(inactivate_user)


def create_activation(sender, instance, created, *args, **kwargs):
    if created and not instance.is_active:
        activation = Activation(
            user=instance,
            token=token_hex(32)
        )
        activation.save()
        send_activation_email(activation)


post_save.connect(create_activation, sender=settings.AUTH_USER_MODEL)
