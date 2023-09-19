from django.db import models


class Author(models.Model):
    pass


class Blog(models.Model):
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=15000)
    recension = models.IntegerField()
    comment = models.CharField(max_length=1024)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
