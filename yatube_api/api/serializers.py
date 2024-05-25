from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model

from posts.models import Comment, Post, Group, Follow

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели публикаций."""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True, required=False
    )

    class Meta:
        fields = '__all__'
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Group."""

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели подписок."""

    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    user = serializers.SlugRelatedField(
        slug_field='username',
        required=False,
        queryset=User.objects.all(),
    )

    def validate(self, data):
        current_user = self.context['request'].user
        followings = current_user.followers.all()
        if current_user.username == data['following'].username:
            raise serializers.ValidationError()
        for follow in followings:
            if data['following'].username == follow.following.username:
                raise serializers.ValidationError()
        return data

    class Meta:
        fields = ('user', 'following')
        model = Follow
