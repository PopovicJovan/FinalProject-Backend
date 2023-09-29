
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import (BlogSerialized, RecensionSerialized,
                          CommentSerialized, UserSerialized,
                          LogInSerialized)

from .models import Blog, Recension, Comment, User
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes,
                                       )

from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User as AuthUser
from django.db import IntegrityError


class BlogsViewSet(ModelViewSet):
    serializer_class = BlogSerialized
    filterset_fields = ["average_rate", "author", "title"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Blog.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(self, request)
        except Http404:
            return Response({"This user does not exist or you are not registered"}, status=404)

    def list(self, request, *args, **kwargs):
        return super().list(self, request)


class RecensionViewSet(ModelViewSet):
    serializer_class = RecensionSerialized
    filterset_fields = ["author", "rate", "blog"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recension.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(self, request)
        except Http404:
            return Response({"This user does not exist or you are not registered"}, status=404)

    def list(self, request, *args, **kwargs):
        return super().list(self, request)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerialized
    filterset_fields = ["author", "blog"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(self, request)
        except Http404:
            return Response({"This user does not exist or you are not registered"}, status=404)

    def list(self, request, *args, **kwargs):
        return super().list(self, request)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerialized
    filterset_fields = ["username"]
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            return super().retrieve(self, request)
        except Http404:
            return Response({"This user does not exist or you are not registered"}, status=404)

    def list(self, request, *args, **kwargs):
        return super().list(self, request)

    def create(self, request, *args, **kwargs):
        username = request.data["username"]
        try:
            tryuser = User.objects.get(username=username)
        except User.DoesNotExist:
            tryuser = None
        if tryuser: return Response({'message:': 'User with that username already existssss'}, status=400)
        return super().create(request, *args, **kwargs)

    # def destroy(self, request, *args, **kwargs):
    #     try:
    #         username = request.data["username"]
    #         password = request.data["password"]
    #         first_name = request.data["first_name"]
    #         last_name = request.data["last_name"]
    #
    #         user = User.objects.get(username=username,
    #                                 first_name=first_name,
    #                                 last_name=last_name,
    #                                 password=password)
    #         user.delete()


class LogInSet(ModelViewSet):
    serializer_class = LogInSerialized

    def get_queryset(self):
        return Token.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            try:
                user = AuthUser.objects.get(username=request.data["username"],
                                            password=request.data["password"])
            except AuthUser.DoesNotExist:
                return Response({'You are not registered!'}, status=400)
            token = Token.objects.create(user=user)
            return Response({'tokenkey': token.key})
        except IntegrityError:
            return Response()


@api_view(['GET'])  # Definirajte HTTP metode koje vaša funkcija podržava (u ovom slučaju samo GET)
@authentication_classes([TokenAuthentication])  # Koristimo TokenAuthentication za ovu funkciju
# @permission_classes([IsAuthenticated])  # Ovo će osigurati da samo autentifikovani korisnici mogu pristupiti funkciji
def iftokenisvalid(request, tokenkey):
    # Ako dođete do ove tačke u kodu, to znači da je token važeći
    if Token.objects.filter(pk=tokenkey).exists():
        return Response({'message': 'Token je važeći.'}, status=200)
    return Response({'message': 'Token nije važeći.'}, status=403)
