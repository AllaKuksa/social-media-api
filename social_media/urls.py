from rest_framework import routers
from django.urls import path, include
from social_media.views import ProfileViewSet

router = routers.DefaultRouter()

router.register("profiles", ProfileViewSet)


urlpatterns = [
    path("", include(router.urls)),
]


app_name = "social_media"
