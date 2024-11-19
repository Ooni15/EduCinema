from django.db import models
from django.conf import settings

class Article(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    related_major = models.CharField(max_length=100, blank=True, null=True)
    movie_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes_count = models.IntegerField(default=0)
    technology_type = models.CharField(max_length=100, blank=True, null=True)
    learning_material_url = models.URLField(blank=True, null=True)
    short_description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title
