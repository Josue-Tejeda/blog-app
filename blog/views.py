from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.views.generic import ListView

from blog.data import PUBLISHED
from .forms import EmailPostForm
from .models import Post

def post_list(request):
    template = 'post/list.html'
    
    post_list = Post.objects.get_published()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try: 
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    
    context = {'posts': posts}
    return render(request, template, context)


class PostListView(ListView):
    """
    Args:
        ListView (Post): View to show list of published posts
    """
    queryset = Post.objects.get_published()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post/list.html'


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


def post_share(request, post_id):
    template = 'post/share.html'
    post = get_object_or_404(
        Post,
        id=post_id,
        status=PUBLISHED
    )
    sent = False
    context = {
        'post': post,
        'form': form,
    }
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                "{cd['name']} recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            sent = True
    else:
        form = EmailPostForm()
    
    context['sent'] = sent
    return render(request, template, context)