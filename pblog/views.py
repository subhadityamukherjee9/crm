from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from mezzanine.blog.views import blog_post_list
from mezzanine.blog.models import BlogPost, BlogCategory
from django.db.models import Q

def post_list(request):
    posts = BlogPost.objects.all()
    query = request.GET.get("q")
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(keywords_string__icontains=query)
        ).distinct()
    return render(request, 'blog.html', {'posts': posts})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'detailed-blog.html', {'post': post})
