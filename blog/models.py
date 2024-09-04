from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager

from blog import data
from blog.managers import PostQuerySet, CommentQuerySet

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
    
    tags = TaggableManager()
    
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
        
    def get_similar_posts(self):
        posts_tags_ids = self.tags.values_list('id', flat=True)
        return Post.objects.get_published().filter(tags__in=posts_tags_ids).exclude(id=self.id)
    

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    
    name = models.CharField(max_length=80)
    
    email = models.EmailField()
    
    body = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True)
    
    objects = CommentQuerySet.as_manager()
    
    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at'])
        ]
        
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'