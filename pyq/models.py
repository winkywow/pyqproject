from django.db import models
from django.shortcuts import render

from account.models import User

per_post = 6


# Create your models here.
class Post(models.Model):
    pid = models.AutoField(primary_key=True)
    user_now = models.ForeignKey(User, on_delete=models.CASCADE)
    context = models.TextField()
    created_time = models.DateTimeField('Created', auto_now_add=True)
    edit_time = models.DateTimeField('Edit', auto_now=True)

    def __str__(self):
        return self.context

    @classmethod
    def post_add(cls, user_login, context):
        p = Post(user_now=user_login, context=context)
        p.save()

    @classmethod
    def post_edit(cls, post_now, context):
        post_now.context = context
        post_now.save()

    @classmethod
    def count_pages(cls, pages):
        tot = Post.objects.count()
        if tot <= pages * per_post:
            return 0
        else:
            return 1

    @classmethod
    def show(cls, request, user_login, pages):
        more_pages = Post.count_pages(pages)
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
