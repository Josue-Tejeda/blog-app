from django.conf import settings
from django.db import models
from django.utils import timezone

from blog import data

class Post(models.Model):
    title = models.CharField(max_length=250)
    
    status = models.SmallIntegerField(
        choices=data.BLOG_STATUS,
        default=data.DRAFT
    )
    
    slug = models.SlugField(max_length=250)
    
    body = models.TextField()
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    
    publish_at = models.DateTimeField(default=timezone.now)
    
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    
    updated_at = models.DateTimeField(auto_now=timezone.now)
    
    class Meta:
        ordering = ['-publish_at']
        indexes = [
            models.Index(fields=['-publish_at'])
        ]
    
    def __str__(self):
        return self.title
