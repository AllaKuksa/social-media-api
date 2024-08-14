import os
import uuid

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField


def profile_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/profiles/", filename)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profiles"
    )
    biography = models.TextField()
    profile_picture = models.ImageField(null=True, upload_to=profile_image_file_path)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    birth_date = models.DateField(null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ["full_name"]


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

    def __str__(self):
        return f"{self.follower} follows {self.following}"


