# Generated by Django 3.0.2 on 2020-05-02 12:38

import django.contrib.auth.password_validation
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200502_1458'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookmark',
            options={'ordering': ['user_id', 'movie_id']},
        ),
        migrations.RenameField(
            model_name='bookmark',
            old_name='movie_id',
            new_name='movie',
        ),
        migrations.RenameField(
            model_name='bookmark',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, validators=[django.contrib.auth.password_validation.UserAttributeSimilarityValidator.validate, django.contrib.auth.password_validation.MinimumLengthValidator.validate, django.contrib.auth.password_validation.NumericPasswordValidator.validate], verbose_name='password'),
        ),
    ]
