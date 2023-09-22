from rest_framework import serializers
from .models import Blog, Recension, Comment, User


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
                  "blog"
                  ]


class CommentSerialized(serializers.ModelSerializer):
    # author = UserSerialized(read_only=True)

    class Meta:
        model = Comment
        fields = ["author", "blog", "content"]
