from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.hashers import make_password
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
        try:
            try:
                Token.objects.get(key=request.auth)
                return super().retrieve(self, request)
            except Token.DoesNotExist: return Response()
        except Http404:
            return Response({"This blog does not exist!"}, status=404)

    def list(self, request, *args, **kwargs):
        try:
            Token.objects.get(key=request.auth)
            return super().list(self, request)
        except Token.DoesNotExist:
            return Response()

    def destroy(self, request, *args, **kwargs):
        blog_author = self.get_object().author.username
        user_sender = Token.objects.get(key=request.auth).user

        if user_sender.is_superuser or user_sender.username == blog_author: return super().destroy(self, request)
        return Response()

    def update(self, request, *args, **kwargs):
        blog_author = self.get_object().author.username
        user_sender = Token.objects.get(key=request.auth).user

        if user_sender.is_superuser or user_sender.username == blog_author:
            blog = Blog.objects.get(id=request.data['id'])
            try:
                blog.content = request.data['content']
            except KeyError: blog.save()
            try:
                if request.data['title']: blog.title = request.data['title']
            except KeyError: blog.save()
            blog.save()
            return Response()
        
        return Response()

    def create(self, request, *args, **kwargs):
        if request.auth:
            author_token = Token.objects.get(key=request.auth).user
            author = User.objects.get(username=author_token)
            Blog.objects.create(author=author,
                                title=request.data['title'],
                                content=request.data['content'])
            return Response()
        return Response({'You have to be logged in!'}, status=403)


class RecensionViewSet(ModelViewSet):
    serializer_class = RecensionSerialized
    filterset_fields = ["author", "rate", "blog"]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self): return Recension.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            try:
                Token.objects.get(key=request.auth)
                return super().retrieve(self, request)
            except Token.DoesNotExist:
                return Response()
        except Http404:
            return Response({"This user does not exist!"}, status=404)

    def list(self, request, *args, **kwargs):
        try:
            Token.objects.get(key=request.auth)
            return super().list(self, request)
        except Token.DoesNotExist:
            return Response()

    def destroy(self, request, *args, **kwargs):
        recension_author = self.get_object().author.username
        user_sender = Token.objects.get(key=request.auth).user

        if user_sender.is_superuser or user_sender.username == recension_author: return super().destroy(self, request)
        return Response()

    def update(self, request, *args, **kwargs):
        recension_author = self.get_object().author.username
        user_sender = Token.objects.get(key=request.auth).user

        if user_sender.is_superuser or user_sender.username == recension_author:
            recension = Recension.objects.get(id=request.data['id'])
            recension.rate = request.data['rate']
            recension.save()
        return Response()

    def create(self, request, *args, **kwargs):
        if request.auth:
            user_sender = Token.objects.get(key=request.auth).user
            author = User.objects.get(username=user_sender)
            try: blog = Blog.objects.get(id=request.data['blog'])
            except Blog.DoesNotExist: return Response({'That blog does not exist!'})

            try: Recension.objects.get(author=author, blog=blog)
            except Recension.DoesNotExist:
                Recension.objects.create(author=author,
                                         rate=request.data['rate'],
                                         blog=blog)
            return Response()

        return Response({'You have to be logged in!'}, status=403)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerialized
    filterset_fields = ["author", "blog"]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self): return Comment.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            try:
                Token.objects.get(key=request.auth)
                return super().retrieve(self, request)
            except Token.DoesNotExist:
                return Response()
        except Http404:
            return Response({"This user does not exist or you are not registered"}, status=404)

    def create(self, request, *args, **kwargs):
        if request.auth:
            author_token = Token.objects.get(key=request.auth).user
            author = User.objects.get(username=author_token)
            blog = Blog.objects.get(id=request.data['blog'])
            Comment.objects.create(author=author,
                                   content=request.data['content'],
                                   blog=blog)
            return Response()
        return Response({'You have to be logged in!'}, status=403)

    def list(self, request, *args, **kwargs):
        try:
            Token.objects.get(key=request.auth)
            return super().list(self, request)
        except Token.DoesNotExist: return Response()

    def destroy(self, request, *args, **kwargs):
        comment_author = self.get_object().author.username
        user_sender = Token.objects.get(key=request.auth).user

        if user_sender.is_superuser or user_sender.username == comment_author: return super().destroy(self, request)

        return Response()

    def update(self, request, *args, **kwargs):
        comment_author = self.get_object().author.username
        user_sender = Token.objects.get(key=request.auth).user

        if user_sender.is_superuser or user_sender.username == comment_author:
            comment = Comment.objects.get(id=request.data['id'])
            comment.content = request.data['content']
            comment.save()

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

        if user_sender.is_superuser or user_sender.username == user: return super().update(self, request)

        return Response()

    def destroy(self, request, *args, **kwargs):
        user = self.get_object().username
        user_sender = Token.objects.get(key=request.auth).user

        if user_sender.is_superuser or user_sender.username == user: return super().destroy(self, request)

        return Response()


class LogInSet(ModelViewSet):
    serializer_class = LogInSerialized

    def get_queryset(self):
        return Token.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            try: user = AuthUser.objects.get(username=request.data['username'])
            except AuthUser.DoesNotExist:
                return Response({'You are not registered!'}, status=400)
            if user.password[0:20] == make_password(request.data['password'])[0:20]:
                token = Token.objects.create(user=user)
                return Response({'tokenkey': token.key})
            return Response({'You are not registered!'}, status=400)
        except IntegrityError: return Response()

    def list(self, request, *args, **kwargs): return Response()
    def retrieve(self, request, *args, **kwargs): return Response()
    def update(self, request, *args, **kwargs): return Response()


class RegisterUser(ModelViewSet):
    serializer_class = UserSerialized

    def get_queryset(self): return User.objects.all()

    def list(self, request, *args, **kwargs): return Response()
    def retrieve(self, request, *args, **kwargs): return Response()
    def destroy(self, request, *args, **kwargs): return Response()
    def update(self, request, *args, **kwargs): return Response()

    def create(self, request, *args, **kwargs):
        username = request.data["username"]
        try: User.objects.get(username=username)
        except User.DoesNotExist:
            User.objects.create(username=request.data["username"],
                                first_name=request.data["first_name"],
                                last_name=request.data["last_name"],
                                password=make_password(request.data["password"]))
            return Response()
        return Response({'That user already exists!'}, status=403)

# -------------------------functions-------------------------------


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def iftokenisvalid(request):
    print(request.auth)
    try:
        Token.objects.get(key=request.auth)
        return Response({'message': 'Token je važeći.'}, status=200)
    except Token.DoesNotExist:
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
    except AuthUser.DoesNotExist: return Response()
