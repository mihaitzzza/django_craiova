from secrets import token_hex
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.sites.models import Site
from django.shortcuts import reverse
from django.utils import timezone
from activation.models import AVAILABILITY_UNIT, AVAILABILITY_VALUE, AVAILABILITY


def send_activation_email(activation):
    user = activation.user
    email = user.email
    first_name = user.first_name
    last_name = user.last_name

    email_template = get_template('activation/email.html')
    email_content = email_template.render({
        'first_name': first_name,
        'last_name': last_name,
        'availability': {
            'unit': AVAILABILITY_UNIT,
            'value': AVAILABILITY_VALUE
        },
        'activation_url': '{HOST}{ACTIVATE_ROUTE}'.format(
            HOST=Site.objects.get_current().domain,
            ACTIVATE_ROUTE=reverse('activation:activate', args=[activation.token])
        )
    })

    mail = EmailMultiAlternatives(
        'Activate your account',
        email_content,
        settings.EMAIL_HOST_USER,
        [email]
    )
    mail.content_subtype = 'html'
    mail.send()


def regenerate_activation(activation):
    activation.token = token_hex(16)
    activation.expires_at = timezone.now() + timezone.timedelta(**AVAILABILITY)
    activation.save()

    send_activation_email(activation)
