from django.db import models
from django.conf import settings
from articles.models import Article

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')  # 중복 좋아요 방지

    def __str__(self):
        return f'Like by {self.user.username} on {self.article.title}'