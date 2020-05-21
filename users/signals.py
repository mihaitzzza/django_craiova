from users.models import MyUser, Profile
from django.db.models.signals import post_save


def create_user_profile(sender, instance, created, **kwargs):
    print('*****************************')
    print('*****************************')
    print('*****************************')
    print('*****************************')
    print('*****************************')
    print('created', created)

    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=MyUser)