from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, User
from django.utils.translation import ugettext_lazy as _
from SmartMovie.settings import AUTH_PASSWORD_VALIDATORS


class Movie(models.Model):
    class Meta:
        ordering = ['movie_id']

    def __str__(self):
        return f'{self.movie_id} [{self.title}]'

    movie_id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    year = models.PositiveIntegerField(null=True, blank=True)
    genres = ArrayField(models.CharField(max_length=63), null=True, blank=True)


class Link(models.Model):
    class Meta:
        ordering = ['movie_id']

    def __str__(self):
        return f'{self.movie}'

    movie = models.OneToOneField(Movie, related_name='links', on_delete=models.CASCADE, primary_key=True)
    imdb_id = models.PositiveIntegerField(null=True, blank=True)
    tmdb_id = models.PositiveIntegerField(null=True, blank=True)


class Rating(models.Model):
    class Meta:
        ordering = ['user_id', 'movie_id']

    def __str__(self):
        return f'{self.user_id}-{self.movie}'

    user_id = models.PositiveIntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5.0)])
    timestamp = models.PositiveIntegerField(null=True, blank=True)
    is_archived = models.BooleanField(default=True)


class Tag(models.Model):
    class Meta:
        ordering = ['user_id', 'movie_id']

    def __str__(self):
        return f'{self.user_id}-{self.movie}'

    user_id = models.PositiveIntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    tag = models.CharField(max_length=127)
    timestamp = models.PositiveIntegerField(null=True, blank=True)


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


def get_password_validators(validator_config):
    from django.utils.module_loading import import_string
    validators = []
    for validator in validator_config:
        try:
            validator_class = import_string(validator['NAME'])
        except ImportError:
            continue
        validators.append(validator_class().validate)

    return validators


class User(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(
        _('password'),
        max_length=128,
        validators=get_password_validators(AUTH_PASSWORD_VALIDATORS)
    )
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Bookmark(models.Model):
    class Meta:
        ordering = ['user_id', 'movie_id']

    def __str__(self):
        return f'{self.user_id}-{self.movie_id}'

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    timestamp = models.PositiveIntegerField(null=True, blank=True)
