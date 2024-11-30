from django.urls import path
from user.views import RegisterView, ProfileView, LogoutView, CustomTokenObtainPairView, CustomTokenRefreshView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('auth/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
]

