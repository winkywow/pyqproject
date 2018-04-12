from django.shortcuts import render, get_object_or_404
from django import forms
from .forms import PostForms
from .models import Post
from account.models import User
from django.http import HttpResponse, Http404


def show(request, user_login):
    posts = list(Post.objects.all())[-1:-7:-1]
    return render(request, 'pyq/index.html', {
        'posts': posts,
        'user_login': user_login,
    })


def index(request, user_sid):
    user_login = get_object_or_404(User, sid=user_sid)
    return show(request, user_login)


def post_action(request, user_sid, post_id):
    user_login = get_object_or_404(User, sid=user_sid)
    if request.method == 'POST':
        if request.POST['type_change'] == 'add':
            post_form = PostForms(request.POST)
            if post_form.is_valid():
                context = post_form.cleaned_data['context']
                nn_post = Post(
                    user_now=user_login,
                    context=context,
                )
                nn_post.save()
        elif request.POST['type_change'] == 'edit':
            # post_id = request.POST['post_id']
            post_now = get_object_or_404(Post, pk=post_id)
            if user_login == post_now.user_now:
                return render(request, 'pyq/edit.html', {
                    'post_edit': post_now,
                    'user_login': user_login,
                })
        elif request.POST['type_change'] == 'delete':
            # post_id = request.POST['post_id']
            post_now = get_object_or_404(Post, pk=post_id)
            if user_login == post_now.user_now or user_login.permission:
                post_now.delete()
        elif request.POST['type_change'] == 'edit_add':
            # post_id = request.POST['post_id']
            post_now = get_object_or_404(Post, pk=post_id)
            if user_login == post_now.user_now:
                post_form = PostForms(request.POST)
                if post_form.is_valid():
                    context = post_form.cleaned_data['context']
                    post_now.context = context
                    post_now.save()
    return show(request, user_login)


'''
def post_edit(request, user_sid, post_id):
    user_login = get_object_or_404(User, sid=user_sid)
    post_now = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        if user_login == post_now.user_now:
            return render(request, 'pyq/edit.html', {
                'post_edit': post_now,
                'user_login': user_login,
            })
    return show(request, user_login)


def post_edit_add(request, user_sid, post_id):
    user_login = get_object_or_404(User, sid=user_sid)
    post_now = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        if user_login == post_now.user_now:
            post_nn = PostForms(request.POST)
            if post_nn.is_valid():
                context = post_nn.cleaned_data['context']
                post_now.context = context
                post_now.save()
    return show(request, user_login)


def post_delete(request, user_sid, post_id):
    user_login = get_object_or_404(User, sid=user_sid)
    post_now = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        if user_login == post_now.user_now or user_login.permission:
            post_now.delete()
    return show(request, user_login)


def post_add(request, user_sid):
    user_login = get_object_or_404(User, sid=user_sid)
    if request.method == 'POST':
        post_form = PostForms(request.POST)
        if post_form.is_valid():
            if request.POST['type_change'] == 'add':
                context = post_form.cleaned_data['context']
                nn_post = Post(
                    user_now=user_login,
                    context=context,
                )
                nn_post.save()
    return show(request, user_login)
'''
