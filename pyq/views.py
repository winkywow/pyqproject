from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse


from .forms import PostForms
from .models import Post
from account.models import User
from account.views import check_session


def get_user_from_request(request):
    user_sid = request.session.get('myUser', None)
    if not user_sid:
        return None
    user_login = get_object_or_404(User, sid=user_sid)
    return user_login


# @check_session
def index(request):
    user_login = get_user_from_request(request)
    if not user_login:
        return HttpResponseRedirect(reverse('account:login'))
    return Post.show(request, user_login, 1)


# @check_session
def post_action(request, pages, post_id):
    user_login = get_user_from_request(request)
    if not user_login:
        return HttpResponseRedirect(reverse('account:login'))
    if request.method == 'POST':
        if request.POST['type_change'] == 'add':
            post_form = PostForms(request.POST)
            if post_form.is_valid():
                context = post_form.cleaned_data['context']
                Post.post_add(user_login, context)
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
                    Post.post_edit(post_now, context)
        elif request.POST['type_change'] == 'load_more':
            pages += 1
    return Post.show(request, user_login, pages)
