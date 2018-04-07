from django.db import models


# Create your models here.
class User(models.Model):
    sid = models.CharField(max_length=50, unique=1)
    username = models.CharField(max_length=50, unique=1)
    password = models.CharField(max_length=50)
    permission = models.BooleanField(default=False)

    def __str__(self):
        return self.username
