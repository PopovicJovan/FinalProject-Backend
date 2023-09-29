from rest_framework import serializers
from .models import Blog, Recension, Comment, User
from django.contrib.auth.models import User as AuthUser
from rest_framework.authtoken.models import Token


class UserSerialized(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "password",
            # "date_joined"
        ]

    # def validate_username(self, username):
    #     if not any(char.isupper() for char in username):
    #         raise serializers.ValidationError( "Username must contain one uppercase at least!")


class SignInSerialized(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ["user", "key"]
        read_only_fields = ["key"]

class LogInSerialized(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password')
    class Meta:
        model = Token
        fields = ["user", "key", "username", "password"]
        read_only_fields = ["key","user"]

class BlogSerialized(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "title",
            "content",
            "average_rate",
            "author",
            "date_created",
            "date_updated"
        ]
        read_only_fields = ["average_rate"]


class RecensionSerialized(serializers.ModelSerializer):
    # author = UserSerialized(read_only=True)

    class Meta:
        model = Recension
        fields = ["author",
                  "rate",
                  "blog",
                  "id"
                  ]
        read_only_fields = ["id"]


class CommentSerialized(serializers.ModelSerializer):
    # author = UserSerialized(read_only=True)

    class Meta:
        model = Comment
        fields = ["author", "blog", "content"]
