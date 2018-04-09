from django.shortcuts import render, get_object_or_404
from django import forms
from .forms import PostForms
from .models import Post
from account.models import User
from django.http import HttpResponse, Http404


# Create your views here.
def index(request, user_id):
    posts = list(Post.objects.all())[-1:-7:-1]
    user_login = get_object_or_404(User, pk=user_id)
    return render(request, 'pyq/index.html', {
        'posts': posts,
        'user_login': user_login,
    })


def post_edit(request, user_id, post_id):
    user_login = get_object_or_404(User, pk=user_id)
    post_now = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        if user_login == post_now.user_now:
            return render(request, 'pyq/edit.html', {
                'post_edit': post_now,
                'user_login': user_login,
            })
    posts = list(Post.objects.all())[-1:-7:-1]
    return render(request, 'pyq/index.html', {
        'posts': posts,
        'user_login': user_login,
    })


def post_edit_add(request, user_id, post_id):
    user_login = get_object_or_404(User, pk=user_id)
    post_now = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        if user_login == post_now.user_now:
            post_nn = PostForms(request.POST)
            if post_nn.is_valid():
                context = post_nn.cleaned_data['context']
                post_now.context = context
                post_now.save()
    posts = list(Post.objects.all())[-1:-7:-1]
    return render(request, 'pyq/index.html', {
        'posts': posts,
        'user_login': user_login,
    })


def post_delete(request, user_id, post_id):
    user_login = get_object_or_404(User, pk=user_id)
    post_now = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        if user_login == post_now.user_now or user_login.permission:
            post_now.delete()
    posts = list(Post.objects.all())[-1:-7:-1]
    return render(request, 'pyq/index.html', {
        'posts': posts,
        'user_login': user_login,
    })


def post_add(request, user_id):
    user_login = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        post_form = PostForms(request.POST)
        if post_form.is_valid():
            context = post_form.cleaned_data['context']
            nn_post = Post(
                user_now=user_login,
                context=context,
            )
            nn_post.save()
    posts = list(Post.objects.all())[-1:-7:-1]
    return render(request, 'pyq/index.html', {
        'posts': posts,
        'user_login': user_login,
    })
