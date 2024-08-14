from rest_framework import routers
from django.urls import path, include
from social_media.views import ProfileViewSet, FollowViewSet

router = routers.DefaultRouter()

router.register("profiles", ProfileViewSet)
router.register("follows", FollowViewSet)

urlpatterns = [
    path("", include(router.urls)),
]


app_name = "social_media"
