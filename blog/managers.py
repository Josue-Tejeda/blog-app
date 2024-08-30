from django.db import models

from blog.data import DRAFT, PUBLISHED


class PostQuerySet(models.QuerySet):
    def get_published(self):
        return self.filter(status=PUBLISHED)
    
    def get_draft(self):
        return self.filter(status=DRAFT)