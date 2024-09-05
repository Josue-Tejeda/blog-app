from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from app import views
from blog.sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.redirect_to_post_list),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('blog/', include('blog.urls', namespace='blog')),
]
