from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from social_media.models import Profile
from social_media.permissions import IsAdminOrIsAuthenticated
from social_media.serializers import ProfileSerializer, ProfileImageSerializer, DetailedProfileSerializer, ProfileListSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = [IsAdminOrIsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAdminOrIsAuthenticated],
        url_path="upload-image"

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
            return DetailedProfileSerializer
        if self.action == "list":
            return ProfileListSerializer
        return ProfileSerializer

