from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    password = models.CharField(max_length=128)
    # date_joined = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.username


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=15000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    average_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    # date_created = models.DateField(auto_now_add=True, null=True)
    # date_updated = models.DateField(auto_now=True, null=True)


class Recension(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.CharField(max_length=1020)
