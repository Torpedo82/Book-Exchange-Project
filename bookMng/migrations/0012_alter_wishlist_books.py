# Generated by Django 3.2.6 on 2021-11-14 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookMng', '0011_alter_wishlist_books'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='books',
            field=models.ManyToManyField(null=True, to='bookMng.Book'),
        ),
    ]
