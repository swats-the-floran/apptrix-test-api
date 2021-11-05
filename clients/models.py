from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    CharField,
    DecimalField,
    ForeignKey,
    ImageField,
    Model,
    SET_NULL,
)
from imagekit.models import ProcessedImageField

from .processors import Watermark
from proj_dating.settings import (
    MEDIA_AVATARS_DIR,
    MEDIA_CLPRODUCTS_DIR,
)


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
    match model. records that one participant (sender) likes another
    (recipient). double match should lead to corresponding actions
    """
    sender = ForeignKey(User, on_delete=CASCADE, related_name='senders')
    recipient = ForeignKey(User, on_delete=CASCADE, related_name='recipients')

    class Meta:
        unique_together = (
            'sender',
            'recipient',
        )


class CLCategory(Model):
    """
    product categories model for citilink 
    """
    name = CharField(max_length=128)
    link = CharField(max_length=256, unique=True)
    parent_category = ForeignKey('self', on_delete=SET_NULL, blank=True, null=True, related_name='children_categories')


class CLProduct(Model):
    """
    product model for citilink products
    """
    category = ForeignKey(CLCategory, on_delete=SET_NULL, blank=True, null=True, related_name='products')
    name = CharField(max_length=1024)
    link = CharField(max_length=512, unique=True)
    price = DecimalField(max_digits=15, decimal_places=2)
    picture = ImageField(upload_to=MEDIA_CLPRODUCTS_DIR, blank=True, null=True)
