from django.shortcuts import get_object_or_404

from rest_framework import viewsets, filters, permissions, pagination

from posts.models import Comment, Follow, Group, Post, User
from .serializers import (CommentSerializer,
                          FollowSerializer,
                          GroupSerializer,
                          PostSerializer,
                          UserSerializer)
from .permissions import AuthorOrReadOnly, ReadOnly


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (ReadOnly,)

    def get_permissions(self):
        if self.action == 'create':
            return (permissions.IsAdminUser(),)
        return super().get_permissions()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        post = get_object_or_404(Post, pk=post_id)
        new_queryset = post.comments.select_related('author').all()
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class FollowViewSet(viewsets.ModelViewSet):
    # queryset = Follow.objects.select_related('user', 'author').all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following',)

    def get_queryset(self):
        following = self.kwargs.get("following")
        new_queryset = User.objects.filter(username=following)
        return new_queryset

    def perform_create(self, serializer):
        following = self.kwargs.get("following")
        following = get_object_or_404(User, username=following)
        serializer.save(user=self.request.user,
                        following=following)
