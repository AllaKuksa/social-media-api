from rest_framework import routers
from django.urls import path, include
from social_media.views import ProfileViewSet, FollowViewSet, PostViewSet

router = routers.DefaultRouter()

router.register("profiles", ProfileViewSet)
router.register("follows", FollowViewSet)
router.register("posts", PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
]


app_name = "social_media"
