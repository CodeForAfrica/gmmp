from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from django.core.mail import get_connection, EmailMultiAlternatives
from django.conf import settings


def send_mass_html_mail(subject, message, html_message, from_email, recipient_list):
    emails = []
    for recipient in recipient_list:
        email = EmailMultiAlternatives(subject, message, from_email, [recipient])
        email.attach_alternative(html_message, 'text/html')
        emails.append(email)
    return get_connection().send_messages(emails)

class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.filter(last_login=None)
        password_reset_form = render_to_string(
            'emails/welcome_password_reset.html', {'SITE_URL': settings.SITE_URL})
        send_mass_html_mail(
            'New account on app.gmmp.ngo',
            '''Hi there''',
            password_reset_form,
            settings.EMAIL_FROM,
            [user.email for user in users]
        )
