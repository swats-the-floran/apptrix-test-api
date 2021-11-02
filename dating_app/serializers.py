from rest_framework.serializers import ModelSerializer

from dating_app.models import User


class UserSerializer(ModelSerializer):
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
