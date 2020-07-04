from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from api.views import UsersViewSet, PublisherViewSet, RegisterViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = SimpleRouter()
router.register(r'users/register', viewset=RegisterViewSet, basename='register')
router.register(r'users', viewset=UsersViewSet, basename='users')
router.register(r'publishers', viewset=PublisherViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/token', TokenObtainPairView.as_view()),
    path('auth/token/refresh', TokenRefreshView.as_view()),
]