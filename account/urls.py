from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignupView.as_view(), name='signup-view'),
    path('users/', UserListView.as_view(), name = 'user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name = 'user-detail'),
    path('profile/', ProfileView.as_view(), name = 'profile-view'),
]