from rest_framework import serializers

from social_media.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "biography",
            "profile_picture",
            "phone_number",
            "birth_date"
        ]
        read_only_fields = ["user"]


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "profile_picture"]


class DetailedProfileSerializer(ProfileSerializer):
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "last_name",
            "biography",
            "profile_picture",
            "email",
            "phone_number",
            "birth_date"
        ]


class ProfileListSerializer(ProfileSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "profile_picture",
        ]
