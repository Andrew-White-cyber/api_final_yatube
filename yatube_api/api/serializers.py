from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model


from posts.models import Comment, Post, Group, Follow

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True, required=False)

    class Meta:
        fields = '__all__'
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):

    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        )

    user = serializers.SlugRelatedField(
        slug_field='username',
        required=False,
        read_only=True,
        )

    class Meta:
        fields = ('user', 'following')
        model = Follow


class UserSerializer(serializers.ModelSerializer):

    following = serializers.StringRelatedField()
    followers = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'following', 'followers')
