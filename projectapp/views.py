from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.hashers import make_password, check_password
from django.db.models.signals import (post_save, post_delete)
from django.dispatch import receiver
from django.http import Http404
from django.db import (IntegrityError, models)

from .models import Blog, Recension, Comment, User

from .serializers import (BlogSerialized, RecensionSerialized,
                          CommentSerialized, UserSerialized,
                          LogInSerialized)

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class BlogsViewSet(ModelViewSet):
    serializer_class = BlogSerialized
    filterset_fields = ["average_rate", "author", "title"]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self): return Blog.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try: return super().retrieve(self, request)
        except Http404:
            return Response({"This user does not exist or you are not registered"}, status=404)

    def list(self, request, *args, **kwargs): return super().list(self, request)

    def destroy(self, request, *args, **kwargs):
        blog_author = self.get_object().author.username
        user_sender = Token.objects.get(key=request.auth).user

        if user_sender.is_superuser: return super().destroy(self, request)
        if user_sender.username == blog_author: return super().destroy(self, request)
        return Response()

    def update(self, request, *args, **kwargs):
        blog_author = self.get_object().author.username
        user_sender = Token.objects.get(key=request.auth).user

        if user_sender.is_superuser: return super().update(self, request)
        if user_sender.username == blog_author: return super().update(self, request)

        return Response()


class RecensionViewSet(ModelViewSet):
    serializer_class = RecensionSerialized
    filterset_fields = ["author", "rate", "blog"]
    authentication_classes = [TokenAuthentication]


    def get_queryset(self): return Recension.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try: return super().retrieve(self, request)
        except Http404:
            return Response({"This user does not exist or you are not registered"}, status=404)

    def list(self, request, *args, **kwargs): return super().list(self, request)

    def destroy(self, request, *args, **kwargs):
        recension_author = self.get_object().author.username
        user_sender = Token.objects.get(key=request.auth).user

        if user_sender.is_superuser: return super().destroy(self, request)
        if user_sender.username == recension_author: return super().destroy(self, request)

        return Response()

    def update(self, request, *args, **kwargs):
        recension_author = self.get_object().author.username
        user_sender = Token.objects.get(key=request.auth).user

        if user_sender.is_superuser: return super().update(self, request)
        if user_sender.username == recension_author: return super().update(self, request)

        return Response()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerialized
    filterset_fields = ["author", "blog"]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self): return Comment.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try: return super().retrieve(self, request)
        except Http404:
            return Response({"This user does not exist or you are not registered"}, status=404)

    def list(self, request, *args, **kwargs): return super().list(self, request)

    def destroy(self, request, *args, **kwargs):
        comment_author = self.get_object().author.username
        user_sender = Token.objects.get(key=request.auth).user

        if user_sender.is_superuser: return super().destroy(self, request)
        if user_sender.username == comment_author: return super().destroy(self, request)

        return Response()

    def update(self, request, *args, **kwargs):
        comment_author = self.get_object().author.username
        user_sender = Token.objects.get(key=request.auth).user

        if user_sender.is_superuser: return super().update(self, request)
        if user_sender.username == comment_author: return super().update(self, request)

        return Response()




class UserViewSet(ModelViewSet):
    serializer_class = UserSerialized
    filterset_fields = ["username"]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self): return User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            user = self.get_object().username
            user_sender = Token.objects.get(key=request.auth).user

            if user_sender.is_superuser: return super().retrieve(self, request)
            if user_sender.username == user: return super().retrieve(self, request)

            return Response()
        except Http404:
            return Response({"This user does not exist!"}, status=404)

    def list(self, request, *args, **kwargs):
        user_sender = Token.objects.get(key=request.auth).user
        if user_sender.is_superuser: return super().list(self, request)
        return Response()

    def create(self, request, *args, **kwargs): return Response()

    def update(self, request, *args, **kwargs):
        user = self.get_object().username
        user_sender = Token.objects.get(key=request.auth).user

        if user_sender.is_superuser: return super().update(self, request)
        if user_sender.username == user: return super().update(self, request)

        return Response()

    def destroy(self, request, *args, **kwargs): return Response()


class LogInSet(ModelViewSet):
    serializer_class = LogInSerialized

    def get_queryset(self):
        return Token.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            try:
                user = AuthUser.objects.get(username=request.data['username'])
            except AuthUser.DoesNotExist:
                return Response({'You are not registered!'}, status=400)
            if (user.password[0:20] == make_password(request.data['password'])[0:20]):
                token = Token.objects.create(user=user)
                return Response({'tokenkey': token.key})
            return Response({'You are not registered!'}, status=400)
        except IntegrityError: return Response()

    def list(self, request, *args, **kwargs): return Response()
    def retrieve(self, request, *args, **kwargs): return Response()


class RegisterUser(ModelViewSet):
    serializer_class = UserSerialized

    def get_queryset(self): return User.objects.all()

    def list(self, request, *args, **kwargs): return Response()
    def retrieve(self, request, *args, **kwargs): return Response()
    def destroy(self, request, *args, **kwargs): return Response()

    def create(self, request, *args, **kwargs):
        username = request.data["username"]
        try:
            tryuser = User.objects.get(username=username)
        except User.DoesNotExist:
            tryuser = None
        if tryuser: return Response({'User with that username already exists'}, status=400)

        User.objects.create(username=request.data["username"],
                            first_name=request.data["first_name"],
                            last_name= request.data["last_name"],
                            password=make_password(request.data["password"]))
        return Response()


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def iftokenisvalid(request, tokenkey):
    if Token.objects.filter(pk=tokenkey).exists():
        return Response({'message': 'Token je važeći.'}, status=200)
    return Response({'message': 'Token nije važeći.'}, status=403)


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


#               USER-AUTHUSER               #

# When user in my model is created , user is auth model will be also created!
@receiver([post_save], sender=User)
def create_user(sender, instance, created, **kwargs):
    if created: AuthUser.objects.create(username=instance.username,
                                        password=instance.password,
                                        date_joined=instance.date_joined)


# When user in my model is deleted , user in auth model will be also deleted!
@receiver([post_delete], sender=User)
def delete_user(sender, instance, **kwargs):
    try:
        AuthUser.objects.get(username=instance.username,
                             password=instance.password).delete()

    except AuthUser.DoesNotExist: pass

# When username or password in my user model is changed ,
# auth User model will also change username or password(put or patch)
@receiver(post_save, sender=User)
def update_user(sender, instance, **kwargs):
    try:
        user = AuthUser.objects.get(date_joined=instance.date_joined)
        user.username = instance.username
        user.password = instance.password
        user.save()
    except AuthUser.DoesNotExist:
        return Response()

