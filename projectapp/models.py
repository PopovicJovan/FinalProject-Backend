from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    password = models.CharField(max_length=16)
    exist_since = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username


class Blog(models.Model):
    title = models.CharField(max_length=32)
    content = models.CharField(max_length=15000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    average_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)

    # def __str__(self):
    #     return self.title


class Recension(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField()
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __call__(self):
        print(self.author)

    # def get_all_rates(self, cls):
    #     return Recension.objects.filter(blog=cls)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.CharField(max_length=1024)

    # def __str__(self):
    #     return self.author


# Define the signal handler to update the average rate when a new Recension is created
@receiver([post_save, post_delete], sender=Recension)
def update_blog_average_rate(sender, instance, **kwargs):
    # Calculate the average rate whenever a Recension is saved or deleted

    blog = instance.blog
    recensions = Recension.objects.filter(blog=blog)
    num_recensions = recensions.count()

    if num_recensions > 0:
        total_rate = recensions.aggregate(models.Sum('rate'))['rate__sum']
        blog.average_rate = total_rate / num_recensions

    blog.save()
