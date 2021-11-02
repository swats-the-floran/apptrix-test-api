from rest_framework.routers import DefaultRouter

from .views import UserCreateMVS


urlpatterns = []


router = DefaultRouter()
router.register('create', UserCreateMVS, basename='create_user')
urlpatterns += router.urls
