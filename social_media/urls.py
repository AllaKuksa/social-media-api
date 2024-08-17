from rest_framework import routers
from django.urls import path, include
from social_media.views import (
    ProfileViewSet,
    PostViewSet,
    FollowViewSet,
    FollowersViewSet,
    FollowingsViewSet,
)

router = routers.DefaultRouter()

router.register("profiles", ProfileViewSet)
router.register("posts", PostViewSet)
router.register("my_followers", FollowersViewSet, basename="followers")
router.register("my_followings", FollowingsViewSet, basename="followings")


urlpatterns = [
    path("", include(router.urls)),
]


app_name = "social_media"
