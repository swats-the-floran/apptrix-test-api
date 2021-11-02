from django.contrib.auth.models import AbstractUser
from django.db.models import (
    #CASCADE,
    CharField,
    #DateTimeField,
    EmailField,
    ForeignKey,
    ImageField,
    #Model,
    #TextField,
)


from proj_dating.settings import MEDIA_AVATARS_DIR

class User(AbstractUser):

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

    avatar = ImageField(upload_to=MEDIA_AVATARS_DIR, blank=True, null=True)

    
    def __str__(self):
        return f"user {self.id}: {self.last_name} {self.first_name}"

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
