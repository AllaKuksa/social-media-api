from rest_framework import serializers

from social_media.models import Profile, Follow, Post


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "full_name",
            "biography",
            "profile_picture",
            "phone_number",
            "birth_date",
        ]
        read_only_fields = ["user"]


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "profile_picture"]


class ProfileDetailedSerializer(ProfileSerializer):
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "biography",
            "profile_picture",
            "email",
            "phone_number",
            "birth_date",
        ]


class ProfileListSerializer(ProfileSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "last_name",
            "profile_picture",
        ]


class FollowSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Follow
        fields = [
            "id",
            "follower",
            "following",
            "created_at"
        ]


class FollowListSerializer(FollowSerializer):
    follower_full_name = serializers.CharField(source='follower.full_name')
    following_full_name = serializers.CharField(source='following.full_name')

    class Meta:
        model = Follow
        fields = [
            "id",
            "follower_full_name",
            "following_full_name",
            "created_at"
        ]


class FollowDetailSerializer(FollowSerializer):
    follower = ProfileDetailedSerializer(read_only=True)
    following = ProfileDetailedSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = [
            "id",
            "follower",
            "following",
            "created_at"
        ]


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    author = serializers.CharField(source="author.full_name")

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "created_at",
            "media",
            "hashtag"
        ]