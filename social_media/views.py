from drf_spectacular.types import OpenApiTypes
from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.viewsets import ReadOnlyModelViewSet

from social_media.models import Profile, Follow, Post, Comment, Like
from social_media.permissions import IsAdminOrIsAuthenticated
from social_media.serializers import (
    ProfileSerializer,
    ProfileImageSerializer,
    ProfileDetailedSerializer,
    ProfileListSerializer,
    PostSerializer,
    PostMediaSerializer,
    FollowSerializer,
    FollowingSerializer,
    FollowerSerializer,
    FollowListSerializer,
    LikeSerializer,
    PostListSerializer,
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().select_related("user")
    permission_classes = [IsAdminOrIsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAdminOrIsAuthenticated],
        url_path="upload-image",
    )
    def upload_images(self, request, pk=None):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["POST", "GET"],
        detail=True,
        permission_classes=[IsAdminOrIsAuthenticated],
        url_path="follow",
    )
    def follow(self, request, pk=None):
        follower = get_object_or_404(Profile, user=request.user)
        following = get_object_or_404(Profile, pk=pk)

        if Follow.objects.filter(follower=follower, following=following).exists():
            return Response({"You have already followed this user"})

        Follow.objects.create(follower=follower, following=following)
        return Response({"You are now following this user"})

    @action(
        methods=["POST", "GET"],
        detail=True,
        permission_classes=[IsAdminOrIsAuthenticated],
        url_path="unfollow",
    )
    def unfollow(self, request, pk=None):
        follower = get_object_or_404(Profile, user=request.user)
        following = get_object_or_404(Profile, pk=pk)

        follow = Follow.objects.filter(follower=follower, following=following)
        if follow:
            follow.delete()
            return Response({"You unfollow this user"})
        return Response({"You haven't followed this user"})

    def get_serializer_class(self):
        if self.action == "upload_image":
            return ProfileImageSerializer
        if self.action == "retrieve":
            return ProfileDetailedSerializer
        if self.action == "list":
            return ProfileListSerializer
        return ProfileSerializer

    def get_queryset(self):
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")
        queryset = self.queryset

        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="first_name",
                type=OpenApiTypes.STR,
                description="Filtering by first name",
            ),
            OpenApiParameter(
                name="last_name",
                type=OpenApiTypes.STR,
                description="Filtering by last name",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related("author__user")

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAdminOrIsAuthenticated],
        url_path="upload-image",
    )
    def upload_images(self, request, pk=None):
        post = self.get_object()
        serializer = self.get_serializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["POST", "GET"],
        detail=True,
        permission_classes=[IsAdminOrIsAuthenticated],
        url_path="liked",
    )
    def like(self, request, pk=None):
        post = self.get_object()
        profile = Profile.objects.get(user=self.request.user)

        if Like.objects.filter(author=profile, post=post).exists():
            return Response({"You already liked this post"})

        like = Like.objects.create(author=profile, post=post)
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=["POST", "GET"],
        detail=True,
        permission_classes=[IsAdminOrIsAuthenticated],
        url_path="unliked",
    )
    def unliked(self, request, pk=None):
        post = self.get_object()
        profile = Profile.objects.get(user=self.request.user)

        like = Like.objects.filter(author=profile, post=post)
        if like:
            like.delete()
            return Response({"You unliked this post"})
        return Response({"You haven't liked this post"})

    @action(
        methods=["GET"],
        detail=False,
        permission_classes=[IsAdminOrIsAuthenticated],
        url_path="liked_posts",
    )
    def liked_post(self, request):
        profile = Profile.objects.get(user=self.request.user)
        liked_posts = profile.likes.select_related("post__author__user")
        queryset = Post.objects.filter(pk__in=liked_posts)
        serializer = PostListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == "upload_image":
            return PostMediaSerializer
        if self.action == "list":
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(author=profile)

    def get_queryset(self):
        user = self.request.user.profiles
        following_profiles = Follow.objects.filter(follower=user).values_list(
            "following", flat=True
        )
        queryset = Post.objects.filter(
            author__in=list(following_profiles) + [user]
        ).select_related("author__user")

        hashtag = self.request.query_params.get("hashtag")

        if hashtag:
            queryset = queryset.filter(hashtag__icontains=hashtag)
        return queryset.distinct()


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all().select_related("follower", "following")
    permission_classes = [IsAdminOrIsAuthenticated]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return FollowListSerializer
        return FollowSerializer

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


class FollowingsViewSet(ReadOnlyModelViewSet):
    serializer_class = FollowingSerializer
    permission_classes = [IsAdminOrIsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.profiles.followings.all()


class FollowersViewSet(ReadOnlyModelViewSet):
    serializer_class = FollowerSerializer
    permission_classes = [IsAdminOrIsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.profiles.followers.all()
