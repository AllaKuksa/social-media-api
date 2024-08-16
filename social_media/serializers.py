from rest_framework import serializers

from social_media.models import Profile, Follow, Post, Comment


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


class FollowingSerializer(serializers.ModelSerializer):
    profile_id = serializers.IntegerField(source="following.id")
    first_name = serializers.CharField(source="following.first_name")
    last_name = serializers.CharField(source="following.last_name")

    class Meta:
        model = Follow
        fields = [
            "profile_id",
            "first_name",
            "last_name"
        ]


class FollowerSerializer(serializers.ModelSerializer):
    profile_id = serializers.IntegerField(source="follower.id")
    first_name = serializers.CharField(source="follower.first_name")
    last_name = serializers.CharField(source="follower.last_name")

    class Meta:
        model = Follow
        fields = [
            "profile_id",
            "first_name",
            "last_name"
        ]


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = [
            "id",
            "follower",
            "following",
            "created_at"
        ]


class ProfileDetailedSerializer(ProfileSerializer):
    email = serializers.EmailField(source="user.email")
    followers = FollowerSerializer(many=True, read_only=True)
    followings = FollowingSerializer(many=True, read_only=True)

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
            "followers",
            "followings",
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


class PostMediaSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ["id", "media"]


class PostListSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = [
            "author",
            "content",
            "created_at",
            "hashtag",
        ]


class CommentSerializer(serializers.ModelSerializer):
    commented_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "author",
            "content",
            "commented_at"
        ]


class CommentListSerializer(CommentSerializer):
    author = serializers.CharField(source="author.full_name")
    post = PostListSerializer(read_only=True)


class CommentDetailSerializer(CommentSerializer):
    post = PostSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "content",
            "commented_at"
        ]