from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import UserSerializer


class UserCreateMVS(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']

    #def create(self, request):
    #    super().create(self, request)
