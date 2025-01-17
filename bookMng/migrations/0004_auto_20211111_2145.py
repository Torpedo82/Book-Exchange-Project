# Generated by Django 3.2.6 on 2021-11-12 05:45

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookMng', '0003_review_wishlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='review',
        ),
        migrations.AddField(
            model_name='review',
            name='book',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bookMng.book'),
        ),
        migrations.AddField(
            model_name='review',
            name='review_book',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='review',
            name='review_headline',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
