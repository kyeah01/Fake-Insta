from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from itertools import chain
from .models import Post, Image, Comment, Hashtag
from .forms import PostForm, ImageForm, CommentForm

# Create your views here.
@login_required
def list(request):
    followings = request.user.followings.all()
    # 1.
    # posts = Post.objects.filter(Q(user__in=followings) | Q(user = request.user.pk)).order_by('-pk')
    # 2.
    # chain_followings = chain(followings, [request.user])
    # posts = Post.objects.filter(user__in=followings).order_by('-pk')
    # 3.
    posts = Post.objects.filter(user__in=(tuple(followings) + (request.user.pk,))).order_by('-pk')
    
    # posts = Post.objects.filter(user__in=request.user.followings.all()).order_by('-pk')
    # posts = get_list_or_404(Post.objects.order_by('-pk'))
    context = {
        'posts' : posts,
        'comment_form' : CommentForm()
    }
    return render(request, 'posts/list.html', context)
    
@login_required
def create(request):
    if request.method =="POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            # hashtag
            for content in post.content.split():
                if content[0] == '#':
                    hashtag = Hashtag.objects.get_or_create(content=content)
                    post.hashtags.add(hashtag[0])
            
            for image in request.FILES.getlist('file'):
                request.FILES['file'] = image
                image_form = ImageForm(files=request.FILES)
                if image_form.is_valid():
                    image = image_form.save(commit=False)
                    image.post = post
                    image.save()
            return redirect('posts:list')
    else:
        post_form = PostForm()
        image_form = ImageForm()
    context = {
        'post_form' : post_form,
        'image_form' : image_form
    }
    return render(request, 'posts/form.html', context)
    
@login_required
def update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if post.user != request.user:
        return redirect('posts:list')
    if request.method == "POST":
        post_form  = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post = post_form.save()
            # hashtag update
            # post.hashtags.exclude()
            post.hashtags.clear()
            for content in post.content.split():
                if content[0] == '#':
                    hashtag = Hashtag.objects.get_or_create(content=content)
                    post.hashtags.add(hashtag[0])
            
            
            return redirect('posts:list')
    else:
        post_form = PostForm(instance=post)
    context = {
        'post_form' : post_form
    }
    return render(request, 'posts/form.html', context)
    
@require_POST
def delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if post.user != request.user:
        return redirect('posts:list')
    post.delete()
    return redirect('posts:list')
    
# comment
@login_required
@require_POST
def comment_create(request, post_pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_pk
        comment.save()
    return redirect('posts:list')
    
@require_POST
def comment_delete(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('posts:list')
    
@login_required
def like(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    
    # 1번
    if request.user in post.like_users.all():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
    return redirect('posts:list')
    
    # 2번
    if post.like_users.filter(pk=request.user.pk).exists():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
    return redirect('posts:list')
    

def explore(request):
    posts = Post.objects.order_by('-pk')
    comment_form = CommentForm()
    context = {
        'posts' : posts,
        'comment_form' : comment_form
    }
    return render(request, 'posts/list.html', context)
    
def hashtag(request, hash_pk):
    hashtag = get_object_or_404(Hashtag, pk=hash_pk)
    posts = hashtag.post_set.order_by('-pk')
    context = {
        'hashtag':hashtag,
        'posts' : posts,
    }
    return render(request, 'posts/hashtag.html', context)