from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    title = models.CharField(max_length=50)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Setting(models.Model):
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, default='avatar.png', upload_to='todo/')
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
