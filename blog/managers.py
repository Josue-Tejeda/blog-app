from django.db import models
from django.db.models import Count

from blog.data import DRAFT, PUBLISHED


class PostQuerySet(models.QuerySet):
    def get_published(self):
        return self.filter(status=PUBLISHED)
    
    def get_draft(self):
        return self.filter(status=DRAFT)
    
    
class CommentQuerySet(models.QuerySet):
    def get_all_active(self):
        return self.filter(is_active=True)