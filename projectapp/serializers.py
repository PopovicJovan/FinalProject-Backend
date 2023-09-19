from rest_framework import serializers
from .models import Blog, Recension, Comment, User


class BlogSerialized(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "title",
            "content",
            "rate",
            "author",
            "date_created",
            "date_updated"
        ]


class RecensionSerialized(serializers.ModelSerializer):
    class Meta:
        model = Recension
        fields = ["author", "rate", "blog"]


class CommentSerialized(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["author", "blog"]


class UserSerialized(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "password",
            "exist_since"
        ]
