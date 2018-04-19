from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q

from .models import User
from .forms import UserFormLogin, UserFormRegister
import hashlib


def md5(tmp):
    m = hashlib.md5()
    m.update(tmp.encode("utf8"))
    return m.hexdigest()


def login(request):
    err = ''
    if request.method == "POST":
        uf = UserFormLogin(request.POST)
        if uf.is_valid():
            user_for_login = uf.cleaned_data['user_for_login']
            password = uf.cleaned_data['password']
            user_result = User.objects.filter(Q(sid=user_for_login) | Q(username=user_for_login))
            if len(user_result) > 0:
                if user_result[0].password == password:
                    return HttpResponseRedirect(reverse('pyq:index', args=(user_result[0].sid,)))
                else:
                    err = "Please input the correct password!"
            else:
                err = "The user doesn't exist!"
    else:
        uf = UserFormLogin()
    return render(request, 'account/login2.html', {
        'uf': uf,
        'error_message': err,
    })


def register(request):
    err = ''
    if request.method == 'POST':
        uf = UserFormRegister(request.POST)
        if uf.is_valid():
            sid = uf.cleaned_data['sid']
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            password1 = uf.cleaned_data['password1']
            user_1 = User.objects.filter(sid=sid)
            user_2 = User.objects.filter(username=username)
            if len(user_1) > 0:
                err = "The Student ID is already exist!"
            elif len(user_2) > 0:
                err = "The Username is already exist!"
            elif password != password1:
                err = "The passwords are inconsistent!"
            else:
                u = User(sid=sid, username=username, password=password)
                u.save()
                return login(request)
    else:
        uf = UserFormRegister()
    return render(request, 'account/register.html', {
            'uf': uf,
            'error_message': err,
    })
