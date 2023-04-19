from allauth.account.signals import email_confirmed
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.template.loader import render_to_string

from board.models import Code


def send_notification(user_email, user_code):
    print('сигнал запустил функцию формирования почты для подтверждения кодом')
    html_content = render_to_string(
        'registration/confirm_code.html',
        {
            'code': user_code,
            'link': 'accounts/login/',
        }
    )
    msg = EmailMultiAlternatives(
        subject='Confirm registration by code',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=user_email,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    print('команда отправки электронной почты пользователю с кодом'
          ' для завершения регистрации выполнена')


@receiver(post_save, sender=User)
def new_user_registered(sender, instance, **kwargs):
    print('работает сигнал для подтверждения кодом')
    if instance.is_active:
        return
    code_for_new_user = Code.objects.create(user=instance)
    code = code_for_new_user.user_code
    mail = instance.user.email
    send_notification(user_email=mail, user_code=code)
    print('почта для подтверждения кодом отправлена по сигналу')