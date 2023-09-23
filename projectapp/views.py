# from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import BlogSerialized, RecensionSerialized, CommentSerialized, UserSerialized
from .models import Blog, Recension, Comment, User


class BlogsViewSet(ModelViewSet):
    serializer_class = BlogSerialized
    filterset_fields = ["average_rate", "author", "title"]

    def get_queryset(self):
        return Blog.objects.all()


class RecensionViewSet(ModelViewSet):
    serializer_class = RecensionSerialized
    filterset_fields = ["author", "rate", "blog"]

    def get_queryset(self):
        return Recension.objects.all()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerialized
    filterset_fields = ["author", "blog"]

    def get_queryset(self):
        return Comment.objects.all()


class UserViewSet(ModelViewSet):
    serializer_class = UserSerialized
    filterset_fields = ["username"]

    def get_queryset(self):
        return User.objects.all()
