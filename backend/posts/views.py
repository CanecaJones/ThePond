from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import Follow
from .models import Post, Like, Repost
from .serializers import PostSerializer


class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedView(generics.ListAPIView):
    """
    GET /api/posts/feed/ -> posts de quem eu sigo + meus próprios posts
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        following_ids = Follow.objects.filter(
            follower=self.request.user
        ).values_list("following_id", flat=True)
        return Post.objects.filter(
            author_id__in=list(following_ids) + [self.request.user.id]
        )


class LikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return Response({"liked": False})
        return Response({"liked": True})


class RepostToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        repost, created = Repost.objects.get_or_create(user=request.user, post=post)
        if not created:
            repost.delete()
            return Response({"reposted": False})
        return Response({"reposted": True})