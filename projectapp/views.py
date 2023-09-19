# from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import BlogSerialized, RecensionSerialized, CommentSerialized, UserSerialized
from .models import Blog, Recension, Comment, User


class BlogsViewSet(ModelViewSet):
    serializer_class = BlogSerialized

    def get_queryset(self):
        return Blog.objects.all()


class RecensionViewSet(ModelViewSet):
    serializer_class = RecensionSerialized

    def get_queryset(self):
        return Recension.objects.all()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerialized

    def get_queryset(self):
        return Comment.objects.all()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerialized

    def get_queryset(self):
        return User.objects.all()
