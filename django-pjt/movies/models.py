from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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
    technologies = models.TextField(max_length=100)
    poster = models.ImageField(upload_to='movie_posters/', blank=True, null=True)  # poster_url 대신 ImageField 사용
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.movie_title