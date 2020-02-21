from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator


class Movie(models.Model):
    class Meta:
        ordering = ['movie_id']

    movie_id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    year = models.PositiveIntegerField(null=True, blank=True)
    genres = ArrayField(models.CharField(max_length=63), null=True, blank=True)


class Link(models.Model):
    class Meta:
        ordering = ['movie_id']

    movie_id = models.OneToOneField(Movie, on_delete=models.CASCADE, primary_key=True)
    imdb_id = models.PositiveIntegerField(null=True, blank=True)
    tmdb_id = models.PositiveIntegerField(null=True, blank=True)


class Rating(models.Model):
    class Meta:
        ordering = ['user_id', 'movie_id']

    user_id = models.PositiveIntegerField()
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5.0)])
    timestamp = models.PositiveIntegerField(null=True, blank=True)


class Tag(models.Model):
    class Meta:
        ordering = ['user_id', 'movie_id']

    user_id = models.PositiveIntegerField()
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    tag = models.CharField(max_length=127)
    timestamp = models.PositiveIntegerField(null=True, blank=True)
