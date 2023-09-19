from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32)
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    password = models.CharField(max_length=16)
    exist_since = models.DateTimeField(auto_now_add=True)


class Blog(models.Model):
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=15000)
    rate = models.IntegerField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    # rate = models.ForeignKey()


class Recension(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
