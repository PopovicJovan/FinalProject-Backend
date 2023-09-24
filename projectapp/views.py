from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import BlogSerialized, RecensionSerialized, CommentSerialized, UserSerialized
from .models import Blog, Recension, Comment, User
from django.http import Http404


class BlogsViewSet(ModelViewSet):
    serializer_class = BlogSerialized
    filterset_fields = ["average_rate", "author", "title"]

    def get_queryset(self):
        return Blog.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(self, request)
        except Http404:
            return Response({"This blog does not exist"}, status=404)

    def list(self, request, *args, **kwargs):
        return super().list(self, request)


class RecensionViewSet(ModelViewSet):
    serializer_class = RecensionSerialized
    filterset_fields = ["author", "rate", "blog"]

    def get_queryset(self):
        return Recension.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(self, request)
        except Http404:
            return Response({"This recension does not exist"}, status=404)

    def list(self, request, *args, **kwargs):
        return super().list(self, request)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerialized
    filterset_fields = ["author", "blog"]

    def get_queryset(self):
        return Comment.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(self, request)
        except Http404:
            return Response({"This comment does not exist"}, status=404)

    def list(self, request, *args, **kwargs):
        return super().list(self, request)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerialized
    filterset_fields = ["username"]

    def get_queryset(self):
        return User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(self, request)
        except Http404:
            return Response({"This user does not exist"}, status=404)

    def list(self, request, *args, **kwargs):
        return super().list(self, request)
