from django.conf import settings
from django.db import models


class Publisher(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='publishers')
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name
