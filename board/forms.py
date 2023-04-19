from django import forms

from .models import Category, Comment, NewsLetter, Code


class NewsForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = [
            'category_news',
            'title',
            'text',
            'upload',
            ]


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = [
            'text',
            ]


class NewsLetterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = [
            'title',
            'text',
        ]


class ConfirmationCodeForm(forms.ModelForm):

    class Meta:
        model = Code
        fields = [
            'code_entered',
            ]