from django.db import models
from django.db.models import Q


# Create your models here.
class User(models.Model):
    sid = models.CharField(max_length=50, unique=1)
    username = models.CharField(max_length=50, unique=1)
    password = models.CharField(max_length=50)
    permission = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    @classmethod
    def verify_login_info(cls, user_for_login, password):
        user_result = User.objects.filter(Q(sid=user_for_login) | Q(username=user_for_login))
        if len(user_result) > 0:
            if user_result[0].password == password:
                return '', user_result
            else:
                err = "Please input the correct password!"
        else:
            err = "The user doesn't exist!"
        return err, user_result

    @classmethod
    def user_add(cls, sid, username, password):
        u = User(sid=sid, username=username, password=password)
        u.save()

    @classmethod
    def verify_register_info(cls, sid, username, password, password1):
        err = ''
        user_1 = User.objects.filter(sid=sid)
        user_2 = User.objects.filter(username=username)
        if len(user_1) > 0:
            err = "The Student ID is already exist!"
        elif len(user_2) > 0:
            err = "The Username is already exist!"
        elif password != password1:
            err = "The passwords are inconsistent!"
        return err
