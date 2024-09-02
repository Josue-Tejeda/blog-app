from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.http import Http404

from blog.data import PUBLISHED
from .models import Post

def post_list(request):
    template = 'post/list.html'
    
    post_list = Post.objects.get_published()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
    
    context = {'posts': posts}
    return render(request, template, context)


def post_detail(request, year, month, day, post_slug):
    template = 'post/detail.html'
    try:
        post = get_object_or_404(
            Post,
            slug=post_slug,
            publish_at__year=year,
            publish_at__month=month,
            publish_at__day=day,
            status=PUBLISHED)
    except:
        raise Http404('No Post found.')
    
    context = {'post': post}
    
    return render(request, template, context)