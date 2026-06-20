from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Post, Comment
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    CommentSerializer,
)


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def post_list_create(request):
    if request.method == 'GET':
        posts = Post.objects.select_related('user').prefetch_related('comments')
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {'message': '로그인이 필요합니다.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = PostDetailSerializer(data=request.data)

        if serializer.is_valid():
            post = serializer.save(user=request.user)
            return Response(
                PostDetailSerializer(post).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def post_detail_update_delete(request, post_id):
    try:
        post = Post.objects.select_related('user').prefetch_related('comments').get(id=post_id)
    except Post.DoesNotExist:
        return Response(
            {'message': '게시글을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        post.view_count += 1
        post.save(update_fields=['view_count'])

        serializer = PostDetailSerializer(post)
        return Response(serializer.data)

    if not request.user.is_authenticated:
        return Response(
            {'message': '로그인이 필요합니다.'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if post.user != request.user:
        return Response(
            {'message': '본인이 작성한 게시글만 수정/삭제할 수 있습니다.'},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == 'PUT':
        serializer = PostDetailSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            updated_post = serializer.save()
            return Response(PostDetailSerializer(updated_post).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        post.delete()
        return Response({'message': '게시글이 삭제되었습니다.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response(
            {'message': '게시글을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = CommentSerializer(data=request.data)

    if serializer.is_valid():
        comment = serializer.save(
            user=request.user,
            post=post
        )
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response(
            {'message': '댓글을 찾을 수 없습니다.'},
            status=status.HTTP_404_NOT_FOUND
        )

    if comment.user != request.user:
        return Response(
            {'message': '본인이 작성한 댓글만 삭제할 수 있습니다.'},
            status=status.HTTP_403_FORBIDDEN
        )

    comment.delete()
    return Response({'message': '댓글이 삭제되었습니다.'})