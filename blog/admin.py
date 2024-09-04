from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish_at', 'status']
    
    list_filter = ['status', 'created_at', 'publish_at', 'author']
    
    search_fields = ['title', 'body']
    
    prepopulated_fields = {'slug': ('title',)}
    
    date_hierarchy = 'publish_at'
    
    ordering = ['status', 'publish_at']
    
    show_facets = admin.ShowFacets.ALWAYS
    
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created_at', 'is_active']
    
    list_filter = ['is_active', 'created_at', 'updated_at']
    
    search_fields = ['name', 'email', 'body']