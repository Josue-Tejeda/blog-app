from django.shortcuts import redirect

def redirect_to_post_list(request):
    return redirect('blog:post_list')