# Generated by Django 3.2.6 on 2021-11-14 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookMng', '0009_alter_wishlist_books'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='books',
            field=models.ManyToManyField(to='bookMng.Book'),
        ),
    ]
