import django.contrib.auth.models
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# import django.contrib as djc
from django.contrib.auth.models import User as AuthUser

# from django.conf import settings
from rest_framework.authtoken.models import Token


class User(models.Model):
    # user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    password = models.CharField(max_length=16)
    # exist_since = models.DateField(auto_now_add=True, null=True, blank=True)
    # groups = models.ManyToManyField(Group, related_name='projectapp_users')
    # user_permissions = models.ManyToManyField(Permission, related_name='projectapp_users')

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
    content = models.CharField(max_length=1020)

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


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        django.contrib.auth.models.User.objects.create(username=instance.username,
                                                       password=instance.password)


@receiver(post_save, sender=AuthUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
