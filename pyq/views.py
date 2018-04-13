from django.shortcuts import render, get_object_or_404
from django import forms
from .forms import PostForms
from .models import Post
from account.models import User
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt


per_post = 6


def count_pages(pages):
    tot = Post.objects.count()
    if tot <= pages * per_post:
        return 0
    else:
        return 1


def show(request, user_login, pages):
    more_pages = count_pages(pages)
    if more_pages:
        posts = list(Post.objects.all())[-1:-(per_post * pages + 1):-1]
    else:
        posts = list(Post.objects.all())[::-1]
    return render(request, 'pyq/index.html', {
        'posts': posts,
        'user_login': user_login,
        'pages': pages,
        'more_pages': more_pages,
    })


def index(request, user_sid):
    user_login = get_object_or_404(User, sid=user_sid)
    return show(request, user_login, 1)


def post_action(request, user_sid, pages, post_id):
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
            post_now = get_object_or_404(Post, pk=post_id)
            if user_login == post_now.user_now:
                return render(request, 'pyq/edit.html', {
                    'post_edit': post_now,
                    'user_login': user_login,
                    'pages': pages,
                })
        elif request.POST['type_change'] == 'delete':
            post_now = get_object_or_404(Post, pk=post_id)
            if user_login == post_now.user_now or user_login.permission:
                post_now.delete()
        elif request.POST['type_change'] == 'edit_add':
            post_now = get_object_or_404(Post, pk=post_id)
            if user_login == post_now.user_now:
                post_form = PostForms(request.POST)
                if post_form.is_valid():
                    context = post_form.cleaned_data['context']
                    post_now.context = context
                    post_now.save()
        elif request.POST['type_change'] == 'load_more':
            pages += 1
    return show(request, user_login, pages)


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
