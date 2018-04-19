from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q

from .models import User
import hashlib


class UserFormLogin(forms.Form):
    user_for_login = forms.CharField(label='username', max_length=50)
    password = forms.CharField(label='password', widget=forms.PasswordInput())


def md5(tmp):
    import hashlib
    m = hashlib.md5()
    m.update(tmp.encode("utf8"))
    return m.hexdigest()


def login(request):
    if request.method == "POST":
        uf = UserFormLogin(request.POST)

        if uf.is_valid():
            user_for_login = uf.cleaned_data['user_for_login']
            password = uf.cleaned_data['password']
            '''
            user_for_login = request.POST.get('username')
            password = request.POST.get('password')
            '''
            user_result = User.objects.filter(Q(sid=user_for_login) | Q(username=user_for_login))
            if len(user_result) > 0:
                if user_result[0].password == password:
                    return HttpResponseRedirect(reverse('pyq:index', args=(user_result[0].sid,)))
                else:
                    return render(request, 'account/login2.html', {
                        'uf': uf,
                        'error_message': "Please input the correct password!",
                    })
            else:
                return render(request, 'account/login2.html', {
                    'uf': uf,
                    'error_message': "The user doesn't exist!",
                })

        else:
            return render(request, 'account/login2.html', {'uf': uf})

    else:
        uf = UserFormLogin()
        return render(request, 'account/login2.html', {'uf': uf})
