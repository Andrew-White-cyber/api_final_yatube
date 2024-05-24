from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django.contrib.auth import get_user_model

from posts.models import Post, Comment, Group, Follow
from .serializers import (
    PostSerializer,
    CommentSerializer,
    GroupSerializer,
    FollowSerializer,
)
from .permissions import IsAuthorOrReadOnly

User = get_user_model()


class PostsViewSet(viewsets.ModelViewSet):
    """ВьюСет для модели публикаций."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_paginated_response(self, data):
        """Пагинация только с параметрами limit или offset."""
        if ('limit' not in self.request.query_params
                or 'offset' not in self.request.query_params):
            return Response(data)
        return Response(
            {
                "count": self.paginator.count,
                "next": self.paginator.get_next_link(),
                "previous": self.paginator.get_previous_link(),
                "results": data,
            }
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Group."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]


class CommentsViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментов."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = self.get_post()
        return post.comments.all()


class FollowCreateList(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """Собственный базовый класс для ВьюСета подписок."""

    pass


class FollowViewSet(FollowCreateList):
    """ВьюСет для модели подписок."""

    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ('following__username',)

    def get_queryset(self):
        queryset = Follow.objects.filter(user=self.request.user)
        return queryset

    def create(self, request):
        """Пользователь не может подписаться на самого себя."""
        serializer = FollowSerializer(data=request.data)
        user = User.objects.get(id=request.user.id)
        followings = user.followers.all()
        if serializer.is_valid():
            following = serializer.validated_data['following'].username
            for follow in followings:
                if following == follow.following.username:
                    return Response(
                        "Вы уже подписаны на данного пользователя !",
                        status=status.HTTP_400_BAD_REQUEST
                    )
            if following == request.user.username:
                return Response(
                    "Нельзя подписаться на самого себя !",
                    status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
