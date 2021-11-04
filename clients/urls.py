from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    MatchMVS,
    UserMVS,
)


urlpatterns = []


#router = DefaultRouter()
#router.register('', MatchMVS, basename='match')
#urlpatterns += router.urls

urlpatterns += [path('create/', UserMVS.as_view({'post': 'create'}), name='create_user')]
urlpatterns += [path('<int:pk>/match/', MatchMVS.as_view({'post': 'match'}), name='create_match')]
