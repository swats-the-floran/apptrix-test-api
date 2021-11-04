from PIL import (
    ImageDraw,
    ImageFont,
)
from rest_framework import serializers
from rest_framework.serializers import (
    HiddenField,
    ModelSerializer,
    ValidationError,
)

from .models import (
    Match,
    User,
)


class UserSerializer(ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    #def update(self, instance, validated_data):
    #    for attr, value in validated_data.items():
    #        if attr == 'password':
    #            instance.set_password(value)
    #        else:
    #            setattr(instance, attr, value)
    #    instance.save()
    #    return instance
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password',
            'email',
            'avatar',
            'gender',
        ]


class MatchSerializer(ModelSerializer):

    sender = HiddenField(default=serializers.CurrentUserDefault())

    def validate(self, data):
        if data['sender'] == self.context['recipient']:
            raise ValidationError('you cannot share your sympathy to yourself.')
        return data

    def create(self, validated_data):
        return Match.objects.create(sender=validated_data['sender'], recipient=self.context['recipient'])
    
    class Meta:
        model = Match
        fields = ['sender']
