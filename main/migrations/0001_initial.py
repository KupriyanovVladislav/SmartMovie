# Generated by Django 3.0.2 on 2020-02-21 09:40

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movie_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('year', models.PositiveIntegerField(blank=True, null=True)),
                ('genres', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=63), blank=True, null=True, size=None)),
            ],
            options={
                'ordering': ['movie_id'],
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('movie', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main.Movie')),
                ('imdb_id', models.PositiveIntegerField(blank=True, null=True)),
                ('tmdb_id', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'ordering': ['movie_id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.PositiveIntegerField()),
                ('tag', models.CharField(max_length=127)),
                ('timestamp', models.PositiveIntegerField(blank=True, null=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Movie')),
            ],
            options={
                'ordering': ['user_id', 'movie_id'],
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.PositiveIntegerField()),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5.0)])),
                ('timestamp', models.PositiveIntegerField(blank=True, null=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Movie')),
            ],
            options={
                'ordering': ['user_id', 'movie_id'],
            },
        ),
    ]
