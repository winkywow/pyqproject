from django.shortcuts import render, get_object_or_404
from django import forms
from .forms import PostForms
from .models import Post
from account.models import User
from django.http import HttpResponse, Http404


# Create your views here.
def index(request, user_id):
    posts = list(Post.objects.all())[-10:]
    user_login = get_object_or_404(User, pk=user_id)
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
    posts = list(Post.objects.all())[-10:]
    return render(request, 'pyq/index.html', {
        'posts': posts,
        'user_login': user_login,
    })
