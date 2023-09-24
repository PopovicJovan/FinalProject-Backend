from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import BlogSerialized, RecensionSerialized, CommentSerialized, UserSerialized
from .models import Blog, Recension, Comment, User
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token


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

    # def list(self, request, *args, **kwargs):
    #     # return super().list(self, request)
    #     all_blogs = Blog.objects.all()
    #     blog_serialized = BlogSerialized(all_blogs, many=True)
    #     if request.user.is_superuser:
    #         return Response(blog_serialized.data, status=200)
    #     return Response({'You do not have permissions do see them'}, status=404)

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


# @api_view(['POST'])
# def signup(request):
#     serializer = UserSerialized(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         user = User.objects.get(username=request.data['username'])
#         user.set_password(request.data['password'])
#         user.save()
#         token = Token.objects.create(user=user)
#         return Response({"token": token.key}, status=200)
#     # return Response(serializer.errors, status=400)