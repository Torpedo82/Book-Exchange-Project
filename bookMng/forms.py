import requests
from django import forms
from django.forms import ModelForm, PasswordInput
from .models import Book, Review, Message
from django.contrib.auth.models import User


# from .models import Search


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
        ]


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = [
            'review_headline',
            'review_book',
            'rating',
        ]


class Account(ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = [
            'reciever',
            'message',
        ]


class MessageForm2(ModelForm):
    class Meta:
        model = Message
        fields = [
            'message',
        ]