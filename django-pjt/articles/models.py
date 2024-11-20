from django.db import models
from django.conf import settings
from movies.models import Movie
from accounts.models import User

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    related_major = models.CharField(max_length=100)
    movie_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    technology_type = models.CharField(max_length=100)
    learning_material_url = models.FileField(upload_to='learning_materials/')
    short_description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title
