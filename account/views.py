from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponseRedirect
from .models import User


def login(request):
    if request.method == "POST":
        uf = UserFormLogin(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']

            user_result = User.objects.filter(username=username)
            if len(user_result) > 0:
                if user_result[0].password == password:
                    return render_to_response('account/success.html', {'operation': 'login'})
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
    return render_to_response('account/login.html', {'uf': uf})


class UserFormLogin(forms.Form):
    username = forms.CharField(label='username', max_length=50)
    password = forms.CharField(label='password', widget=forms.PasswordInput())
