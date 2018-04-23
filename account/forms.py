from django import forms


class UserFormLogin(forms.Form):
    user_for_login = forms.CharField(label='username', max_length=50)
    password = forms.CharField(label='password', widget=forms.PasswordInput())


class UserFormRegister(forms.Form):
    sid = forms.CharField(label='Student ID', max_length=50)
    username = forms.CharField(label='Username', max_length=50)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password1 = forms.CharField(label='Password Again', widget=forms.PasswordInput())
