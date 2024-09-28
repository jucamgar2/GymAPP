from django.urls import path
from .views import UserView
from .views import LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', UserView.as_view(), name='user_view'),
    path('login', LoginView.as_view(), name='login_view'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]