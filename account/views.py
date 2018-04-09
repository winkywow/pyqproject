from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import User


class UserFormLogin(forms.Form):
    # sid = forms.CharField(label='sid', max_length=50)
    username = forms.CharField(label='username', max_length=50)
    password = forms.CharField(label='password', widget=forms.PasswordInput())


def login(request):
    if request.method == "POST":
        uf = UserFormLogin(request.POST)
        if uf.is_valid():
            # sid = uf.cleaned_data['sid']
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']

            user_result = User.objects.filter(username=username)
            if len(user_result) > 0:
                if user_result[0].password == password:
                    return HttpResponseRedirect(reverse('pyq:index', args=(user_result[0].id,)))
                else:
                    return render(request, 'account/login.html', {
                        'uf': uf,
                        'error_message': "Please input the correct password!",
                    })
            else:
                return render(request, 'account/login.html', {
                    'uf': uf,
                    'error_message': "The user doesn't exist!",
                })
    else:
        uf = UserFormLogin()
        return render(request, 'account/login.html', {'uf': uf})
