from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import User
from .forms import UserFormLogin, UserFormRegister
import hashlib


def md5(tmp):
    m = hashlib.md5()
    m.update(tmp.encode("utf8"))
    return m.hexdigest()


def check_session(func):
    def wrapper(request, *aaa, **kv):
        user_info = request.session.get('myUser', None)
        if user_info != list(kv.values())[0]:
            return HttpResponseRedirect(reverse('account:login'))
        return func(request, *aaa, **kv)
    return wrapper


def login(request):
    err = ''
    if request.method == "POST":
        uf = UserFormLogin(request.POST)
        if uf.is_valid():
            user_for_login = uf.cleaned_data['user_for_login']
            password = uf.cleaned_data['password']
            err, user_result = User.verify_login_info(user_for_login, password)
            if err == '':
                request.session['myUser'] = user_result[0].sid
                return HttpResponseRedirect(reverse('pyq:index'))
    else:
        uf = UserFormLogin()
    return render(request, 'account/login2.html', {
        'uf': uf,
        'error_message': err,
    })


def logout(request):
    try:
        del request.session['myUser']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('account:login'))


def register(request):
    err = ''
    if request.method == 'POST':
        uf = UserFormRegister(request.POST)
        if uf.is_valid():
            sid = uf.cleaned_data['sid']
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            password1 = uf.cleaned_data['password1']
            err = User.verify_register_info(sid, username, password, password1)
            if err == '':
                User.user_add(sid, username, password)
                return HttpResponseRedirect(reverse('account:login'))
    else:
        uf = UserFormRegister()
    return render(request, 'account/register.html', {
            'uf': uf,
            'error_message': err,
    })
