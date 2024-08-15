from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter

from social_media.models import Profile, Follow, Post, Comment
from social_media.permissions import IsAdminOrIsAuthenticated
from social_media.serializers import (
    ProfileSerializer,
    ProfileImageSerializer,
    ProfileDetailedSerializer,
    ProfileListSerializer,
    FollowSerializer,
    FollowListSerializer,
    FollowDetailSerializer,
    PostSerializer,
    PostMediaSerializer, CommentSerializer, CommentListSerializer, CommentDetailSerializer
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

        ]
    )


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all().select_related("follower__user", "following__user")
    permission_classes = [IsAdminOrIsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return FollowListSerializer
        if self.action == "retrieve":
            return FollowDetailSerializer
        return FollowSerializer


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

    def get_serializer_class(self):
        if self.action == "upload_image":
            return PostMediaSerializer
        return PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().select_related("author__user", "post__author__user")

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListSerializer
        if self.action == "retrieve":
            return CommentDetailSerializer
        return CommentSerializer
