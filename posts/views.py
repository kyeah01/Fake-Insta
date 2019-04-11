from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Post
from .forms import PostForm

# Create your views here.
def list(request):
    posts = get_list_or_404(Post.objects.order_by('-pk'))
    context = {
        'posts' : posts
    }
    return render(request, 'posts/list.html', context)
    
def create(request):
    if request.method =="POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
    else:
        form = PostForm()
    context = {
        'form' : form
    }
    return render(request, 'posts/form.html', context)
    
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        form  = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
    else:
        form = PostForm(instance=post)
    context = {
        'form' : form
    }
    return render(request, 'posts/form.html', context)
    
@require_POST
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.delete()
    return redirect('posts:list')