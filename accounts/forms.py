from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from allauth.account.forms import SignupForm

from board.models import Code


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )



class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)
        user_email = [user.email]

        code_for_new_user = Code.objects.create(user=user)
        code = code_for_new_user.user_code

        html_content = render_to_string(
            'registration/confirm_code.html',
            {
                'link': f'{settings.SITE_URL}/confirm/',
                'user': user,
                'code': code,
            }
        )

        msg = EmailMultiAlternatives(
            subject='Вы успешно зарегистрировались на нашем сайте!',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=user_email
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()

        return user