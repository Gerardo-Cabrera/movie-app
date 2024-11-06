# movies/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.utils.text import slugify
import re
User = settings.AUTH_USER_MODEL

class Genre(models.Model):
    genre_id = models.IntegerField(db_index=True, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    movie_id = models.BigIntegerField(db_index=True, unique=True)
    title = models.CharField(max_length=255)
    date = models.CharField(max_length=10)
    genre = models.ManyToManyField(Genre, related_name='movies')
    popularity = models.DecimalField(max_digits=7, decimal_places=2)
    poster_path = models.URLField()
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            cleaned_title = re.sub(r'[^\w\s]', '', self.title)
            self.slug = slugify(cleaned_title.lower().replace('&', 'and'))
        super(Movie, self).save(*args, **kwargs)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'movie')

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])

    def __str__(self):
        return f"Review by {self.user.username} on {self.movie.title}"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    