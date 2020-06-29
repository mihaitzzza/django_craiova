from django.db import models
from django.conf import settings


class StripeCustomer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stripe_data')
    customer_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.customer_id


class StripeCard(models.Model):
    customer = models.ForeignKey(StripeCustomer, on_delete=models.CASCADE, related_name='cards')
    card_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.card_id
