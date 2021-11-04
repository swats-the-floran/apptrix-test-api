from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
#from rest_framework.filters import SearchFilter
from rest_framework.authentication import (
    BasicAuthentication,
)
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import (
    Match,
    User,
)
from .serializers import (
    MatchSerializer,
    UserSerializer,
)
from proj_dating.settings import EMAIL_HOST_USER


class UserMVS(ModelViewSet):
    """
    heritated from ModelViewSet though the only http method used here is post. but it's easy to add others.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post']

    filter_backends = [
        DjangoFilterBackend,
    #    SearchFilter,
    ]
    filterset_fields = ['gender', 'first_name', 'last_name']
    #search_fields = ['first_name', 'last_name']


class MatchMVS(ModelViewSet):

    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    http_method_names = ['post']

    @action(detail=True, methods=['POST'], name='send_your_match')
    def match(self, request, pk=None):
        sender = request.user
        recipient = User.objects.get(pk=pk)

        serializer = MatchSerializer(context={'recipient': recipient, 'request': request}, data=request.data)
        data_valid = serializer.is_valid(raise_exception=True)
        if data_valid:
            serializer.save()
        
        reverse_match = Match.objects.filter(sender=recipient, recipient=sender)
        if reverse_match:
            send_mail(
                f'Добрый день, {sender.first_name}',
                f'Вы понравились {recipient.first_name}! Почта участника: {recipient.email}',
                EMAIL_HOST_USER,
                [sender.email],
                fail_silently=False,
            )
            send_mail(
                f'Добрый день, {recipient.first_name}',
                f'Вы понравились {sender.first_name}! Почта участника: {sender.email}',
                EMAIL_HOST_USER,
                [recipient.email],
                fail_silently=False,
            )
            
            return Response(recipient.email, 201)
        else:
            return Response(f'your sympathy had been sent to the user {recipient.username}.', 201)
