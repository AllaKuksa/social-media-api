import os
import uuid

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField


def profile_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/airplanes/", filename)


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
