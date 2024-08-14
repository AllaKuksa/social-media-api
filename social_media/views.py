from rest_framework import viewsets

from social_media.models import Profile
from social_media.permissions import IsAdminOrIsAuthenticated
from social_media.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminOrIsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


