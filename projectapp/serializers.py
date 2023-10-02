from rest_framework import serializers
from .models import (Blog, Recension, Comment, User)
from rest_framework.authtoken.models import Token


class UserSerialized(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ["id", "date_joined"]

class LogInSerialized(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password')

    class Meta:
        model = Token
        fields = ["user", "key", "username", "password"]
        read_only_fields = ["key", "user"]


class BlogSerialized(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
        read_only_fields = ["average_rate", "id", "date_created", "date_updated"]


class RecensionSerialized(serializers.ModelSerializer):
    class Meta:
        model = Recension
        fields = '__all__'
        read_only_fields = ["id"]


class CommentSerialized(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ["id"]
