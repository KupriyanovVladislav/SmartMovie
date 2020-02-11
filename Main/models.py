from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator


class Movie(models.Model):
    movie_id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    year = models.PositiveIntegerField(null=True, blank=True)
    genres = ArrayField(models.CharField(max_length=50), null=True, blank=True)


class Link(models.Model):
    movie_id = models.OneToOneField(Movie.movie_id, on_delete=models.CASCADE)
    imdb_id = models.PositiveIntegerField(null=True, blank=True)
    tmdb_id = models.PositiveIntegerField(null=True, blank=True)


class Rating(models.Model):
    user_id = models.PositiveIntegerField()
    movie_id = models.OneToOneField(Movie.movie_id, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5.0)])
    timestamp = models.PositiveIntegerField(null=True, blank=True)


class Tag(models.Model):
    user_id = models.PositiveIntegerField()
    movie_id = models.OneToOneField(Movie.movie_id, on_delete=models.CASCADE)
    tag = models.CharField(max_length=100)
    timestamp = models.PositiveIntegerField(null=True, blank=True)
