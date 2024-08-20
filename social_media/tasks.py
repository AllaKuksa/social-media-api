from celery import shared_task
from social_media.models import Post


@shared_task
def create_post(params) -> None:
    params.pop("scheduled_in", None)
    Post.objects.create(**params)
