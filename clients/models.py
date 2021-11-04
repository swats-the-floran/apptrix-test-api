from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    #ImageField,
    Model,
)
from imagekit.models import ProcessedImageField

from .processors import Watermark
from proj_dating.settings import MEDIA_AVATARS_DIR


class User(AbstractUser):
    """
    user class heritated from AbstractUser. adds gender (enum) and avatar
    (ImageField) fields. adds watermark on avatar image upload.
    """
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = [
        (MALE, 'male'),
        (FEMALE, 'female'),
    ]
    gender = CharField(
        max_length=1,
        choices=GENDERS,
    )

    avatar = ProcessedImageField(
        upload_to=MEDIA_AVATARS_DIR,
        blank=True,
        null=True,
        processors=[Watermark()]
    )

    def __str__(self):
        return f"user {self.id}: {self.last_name} {self.first_name}"

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'


class Match(Model):
    """
    model class. records that one participant (sender) likes another
    (recipient). double match should lead to corresponding actions
    """
    sender = ForeignKey(User, on_delete=CASCADE, related_name='senders')
    recipient = ForeignKey(User, on_delete=CASCADE, related_name='recipients')

    class Meta:
        unique_together = (
            'sender',
            'recipient',
        )
