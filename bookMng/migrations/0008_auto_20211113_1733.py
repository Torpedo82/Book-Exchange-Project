# Generated by Django 3.2.6 on 2021-11-14 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookMng', '0007_auto_20211113_1644'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='bookID',
        ),
        migrations.AddField(
            model_name='wishlist',
            name='books',
            field=models.ManyToManyField(to='bookMng.Book'),
        ),
    ]
