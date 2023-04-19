from django.db import models
from django.contrib.auth.models import User
from .validators import validate_not_empty
import random


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.authorUser.username


class Category(models.Model):
    TYPE_CHOICES = [
        ('Танки', 'Танки'),
        ('Хилы', 'Хилы'),
        ('DD', 'ДД'),
        ('Merchants', 'Торговцы'),
        ('Guildmasters', 'Гилдмастеры'),
        ('Questgivers', 'Квестгиверы'),
        ('Blacksmiths', 'Кузнецы'),
        ('Leatherworkers', 'Кожевники'),
        ('Potions Masters', 'Зельевары'),
        ('Spellmasters', 'Мастера заклинаний'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    category_news = models.CharField(max_length=64, choices=TYPE_CHOICES, default='Tanks')
    title = models.CharField(max_length=128, validators=[validate_not_empty])
    text = models.TextField(validators=[validate_not_empty])
    time = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(upload_to='uploads/', blank=True)

    def preview(self):
        preview = f'{self.text[0:64]}...'
        return preview

    def __str__(self):
        return f'{self.title}: {self.text[:256]}'

    def get_absolute_url(self):
        return f'/news/{self.pk}'


class Comment(models.Model):
    commentPost = models.ForeignKey(Category, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'фрагмент текста отклика: {self.text[:128]}'

    def preview(self):
        preview = f'{self.text[0:64]}...'
        return preview


class Code(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_status = models.BooleanField(default=False)
    user_code = models.CharField(max_length=4, default=str(random.randint(1000, 9999)))
    code_entered = models.CharField(max_length=4, default='')


class NewsLetter(models.Model):
    userNewsletter = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, validators=[validate_not_empty])
    text = models.TextField(validators=[validate_not_empty])
    dateCreation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}: {self.text[:256]}...'