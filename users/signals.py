import stripe
from users.models import Profile
from django.conf import settings
from django.db.models.signals import post_save
from payments.models import StripeCustomer


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def create_stripe_customer(sender, instance, created, **kwargs):
    if created:
        customer = stripe.Customer.create(
            email=instance.email,
            name=f'{instance.first_name} {instance.last_name}',
            api_key=settings.STRIPE_SECRET_KEY,
        )

        StripeCustomer(user=instance, customer_id=customer['id']).save()


post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)
post_save.connect(create_stripe_customer, sender=settings.AUTH_USER_MODEL)