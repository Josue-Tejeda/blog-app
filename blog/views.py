from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from taggit.models import Tag   

from blog.data import PUBLISHED
from .forms import EmailPostForm, CommentForm, SearchForm
from .models import Post

def post_list(request, tag_slug=None):
    template = 'post/list.html'
    
    post_list = Post.objects.get_published()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page', 1)
    try: 
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    
    context = {
        'posts': posts,
        'tag': tag
        }
    return render(request, template, context)


def post_search(request):
    template = 'post/search.html'
    form = SearchForm()
    query = None
    results = []
    
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
                ).filter(search=query).order_by('-rank')
    
    context = {
        'form': form,
        'query': query,
        'results': results
    }
    
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
    
    comments = post.comments.get_all_active()
    form = CommentForm()
    
    similar_posts = post.get_similar_posts().annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish_at')[:4]
    
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts
        }
    
    return render(request, template, context)


def post_share(request, post_id):
    template = 'post/share.html'
    post = get_object_or_404(
        Post,
        id=post_id,
        status=PUBLISHED
    )
    sent = False
    
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            
            
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['email_to']]
            )
            sent = True
    else:
        form = EmailPostForm()
    
    context = {
        'post': post,
        'form': form,
        'sent': sent,
    }
    return render(request, template, context)


@require_POST
def post_comment(request, post_id):
    template = 'post/comment.html'
    
    post = get_object_or_404(
        Post,
        id=post_id,
        status=PUBLISHED
    )
    comment = None
    
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        
    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
        
    return render(request, template, context)