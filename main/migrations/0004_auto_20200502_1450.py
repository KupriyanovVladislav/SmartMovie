# Generated by Django 3.0.2 on 2020-05-02 11:50

import django.contrib.auth.password_validation
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200404_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='is_archived',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, validators=[django.contrib.auth.password_validation.UserAttributeSimilarityValidator.validate, django.contrib.auth.password_validation.MinimumLengthValidator.validate, django.contrib.auth.password_validation.NumericPasswordValidator.validate], verbose_name='password'),
        ),
    ]
