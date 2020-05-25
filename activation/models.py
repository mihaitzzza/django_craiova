from django.conf import settings
from django.db import models
from django.utils import timezone

AVAILABILITY_UNIT = 'minutes'
AVAILABILITY_VALUE = 30
AVAILABILITY = {
    AVAILABILITY_UNIT: AVAILABILITY_VALUE,
}


class Activation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(null=False, max_length=255)
    expires_at = models.DateTimeField(null=False, default=timezone.now() + timezone.timedelta(**AVAILABILITY))
    activated_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.token
