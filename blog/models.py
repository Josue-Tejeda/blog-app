from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from blog import data
from blog.managers import PostQuerySet

class Post(models.Model):
    title = models.CharField(max_length=250)
    
    status = models.SmallIntegerField(
        choices=data.BLOG_STATUS,
        default=data.DRAFT
    )
    
    slug = models.SlugField(
        max_length=250,
        unique_for_date='publish_at'
        )
    
    body = models.TextField()
    
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    
    publish_at = models.DateTimeField(default=timezone.now)
    
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    
    updated_at = models.DateTimeField(auto_now=timezone.now)
    
    objects = PostQuerySet.as_manager()
    
    class Meta:
        ordering = ['-publish_at']
        indexes = [
            models.Index(fields=['-publish_at'])
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish_at.year,
                self.publish_at.month,
                self.publish_at.day,
                self.slug
                ]
            )
    
