from django.urls import path
from rest_framework.routers import SimpleRouter
from django.urls import include

from .views import PostsViewSet, GroupViewSet, CommentsViewSet, FollowViewSet

router_v1 = SimpleRouter()
router_v1.register(r'posts', PostsViewSet)
router_v1.register(r'groups', GroupViewSet)
router_v1.register(r'follow', FollowViewSet, basename='follow')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls)),
]
