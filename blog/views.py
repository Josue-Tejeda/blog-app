from django.shortcuts import get_object_or_404, render
from django.http import Http404

from blog.data import PUBLISHED
from .models import Post

def post_list(request):
    template = 'post/list.html'
    posts = Post.objects.get_published()
    context = {'posts': posts}
    return render(request, template, context)


def post_detail(request, id):
    template = 'post/detail.html'
    try:
        post = get_object_or_404(Post, id=id, status=PUBLISHED)
    except:
        raise Http404('No Post found.')
    
    context = {'post': post}
    
    return render(request, template, context)