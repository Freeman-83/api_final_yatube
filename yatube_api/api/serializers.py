from rest_framework import serializers
from rest_framework.relations import SlugRelatedField, StringRelatedField


from posts.models import Comment, Follow, Group, Post, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'created', 'post')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='follower'
    )
    following = serializers.SlugRelatedField(
        read_only=True, many=True, slug_field='following', allow_null=True
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow
