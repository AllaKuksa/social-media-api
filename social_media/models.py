import os
import uuid

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError


def profile_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.first_name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/profiles/", filename)


def profile_media_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.content)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/media/", filename)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profiles"
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    biography = models.TextField()
    profile_picture = models.ImageField(
        null=True, blank=True, upload_to=profile_image_file_path
    )
    phone_number = PhoneNumberField(unique=True)
    birth_date = models.DateField(null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ["first_name", "last_name"]
        verbose_name_plural = "profiles"


class Follow(models.Model):
    follower = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="followers"
    )
    following = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="followings"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        unique_together = ["follower", "following"]

    @staticmethod
    def validate_follow(follower, following, error_to_raise):
        if follower == following:
            raise error_to_raise("You can't follow yourself")

    def clean(self):
        Follow.validate_follow(self.following, self.follower, ValidationError)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Follow, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.follower} follows {self.following}"


class Post(models.Model):

    class HashtagChoices(models.TextChoices):
        LOVE = "Love"
        LIFE = "Life"
        INSPIRATION = "Inspiration"
        TRAVEL = "Travel"
        FITNESS = "Fitness"
        FOOD = "Food"

    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    media = models.ImageField(null=True, blank=True, upload_to=profile_media_file_path)
    hashtag = models.CharField(max_length=50, choices=HashtagChoices.choices)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post by {self.author}: {self.content}"


class Comment(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-commented_at"]

    def __str__(self):
        return f"Comment by {self.author} at {self.commented_at}"


class Like(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["author", "post"]
        ordering = ["-liked_at"]

    def __str__(self):
        return f"Like by {self.author} at {self.liked_at}"
