import requests
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class MainMenu(models.Model):
    item = models.CharField(max_length=200, unique=True)
    link = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.item


class Book(models.Model):
    name = models.CharField(max_length=200)
    web = models.URLField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    publishdate = models.DateField(auto_now=True)
    picture = models.FileField(upload_to='bookEx/static/uploads')
    pic_path = models.CharField(max_length=300, editable=False, blank=True)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    identification = models.CharField(max_length=200, default="")  # added

    def __str__(self):
        return str(self.id)


class WishlistBook(models.Model):
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, blank=True, null=True, on_delete=models.CASCADE)
    compareID = models.CharField(max_length=200, default="")  # added

    def str(self):
        return str(self.id)


class Review(models.Model):
    book = models.ForeignKey(Book, blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    review_headline = models.CharField(max_length=200, default="")
    review_book = models.CharField(max_length=200, default="")
    rating = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    book = models.ForeignKey(Book, blank=True, null=True, on_delete=models.CASCADE)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


    def __str__(self):
        return str(self.id)


class Message(models.Model):
    sender = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="sender")
    reciever = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="reciever")
    message = models.CharField(max_length=350, default="", blank=True, null=True)
    time_rec = models.DateTimeField(auto_now_add=True)

    def str(self):
        return str(self.id)
