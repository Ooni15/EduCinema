from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Technology(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Technologies"

class Movie(models.Model):
    movie_title = models.CharField(max_length=200)
    movie_genre = models.CharField(max_length=50)
    movie_synopsis = models.TextField()
    movie_rating = models.FloatField(
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ]
    )
    technologies = models.ManyToManyField(Technology, related_name='movies')
    poster_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.movie_title