from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail

from .models import Comment, NewsLetter, Code


def send_notification(preview, pk, post_commented_preview, post_author_email):
    html_content = render_to_string(
        'signals/comment_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/comments/{pk}',
            'post': post_commented_preview,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Post commented/Отклик на объявление',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[post_author_email, ],
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    print('команда отправки электронной почты автору об отклике на объявление выполнена')


@receiver(post_save, sender=Comment)
def notify_about_new_comment(sender, instance, **kwargs):
    post_preview = instance.commentPost.preview()
    author_email = instance.commentPost.author.authorUser.email
    send_notification(instance.preview(), instance.pk, post_preview, author_email)


@receiver(pre_save, sender=Comment)
def notify_comment_accepted(sender, instance, **kwargs):
    if not instance.status:
        return
    mail = instance.commentUser.email

    send_mail(
        subject='Comment accepted/Отклик принят',
        message='Your comment is accepted by the author/Ваш отклик принят автором',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[mail],
        fail_silently=False,
    )
    print('команда отправки электронной почты пользователю, что его отклик принят автором, выполнена')


@receiver(pre_save, sender=NewsLetter)
def newsletter_from_managers(sender, instance, **kwargs):
    users = User.objects.filter(groups__name='common users')
    print(f'объекты users = {users}')
    users = [s.email for s in users]
    print(f'электронная почта users = {users}')

    send_mail(
        subject=str(instance.title),
        message=str(instance.text),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=users,
        fail_silently=False,
    )
    print('команда отправки новостной рассылки пользователям, выполнена')


@receiver(pre_save, sender=Code)
def code_check(sender, instance, **kwargs):
    print('сработал сигнал по модулю Code')
    code_entered_ = instance.code_entered
    user_code_ = instance.user_code
    print(f'code_entered = {code_entered_}, user_code = {user_code_}, status = {instance.user_status}')
    if code_entered_ == user_code_:
        instance.user_status = True
        print(f'код введен правильный, status = {instance.user_status}')