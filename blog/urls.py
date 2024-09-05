from django.urls import path
from . import views
from .feeds import LatestPostFeed
app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post_slug>',
        views.post_detail, 
        name='post_detail'
    ),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment', views.post_comment, name='post_comment'),
    path('feed/', LatestPostFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
]
