from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'post',
            'user',
            'username',
            'content',
            'created_at',
        )
        read_only_fields = ('post', 'user', 'username', 'created_at')


class PostListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'category',
            'username',
            'view_count',
            'comment_count',
            'created_at',
            'updated_at',
        )

    def get_comment_count(self, obj):
        return obj.comments.count()


class PostDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'content',
            'category',
            'user',
            'username',
            'view_count',
            'comments',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('user', 'username', 'view_count', 'comments', 'created_at', 'updated_at')