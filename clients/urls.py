from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    MatchMVS,
    UserMVS,
)



urlpatterns = [
    path('clients/create/', UserMVS.as_view({'post': 'create'}), name='create_user'),
    path('list/', UserMVS.as_view({'get': 'list'}), name='users_list'),
    path('clients/<int:pk>/match/', MatchMVS.as_view({'post': 'match'}), name='create_match'),
]
