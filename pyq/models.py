from django.db import models
from account.models import User


# Create your models here.
class Post(models.Model):
    pid = models.IntegerField(default=0, unique=1)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    context = models.TextField()
    created_time = models.DateTimeField('Created', auto_now_add=True)
    edit_time = models.DateTimeField('Edit', auto_now=True)

    def __str__(self):
        return self.pid
