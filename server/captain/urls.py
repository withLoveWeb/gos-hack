from django.urls import path

from captain.views import (
    RegisterCaptainView,
    CaptainLoginView,
)


urlpatterns = [
    path('register/', RegisterCaptainView.as_view(), name='registercap'),
    path('auth/', CaptainLoginView.as_view(), name='logincap'),
    # path('auth/refresh/', CaptainTokenRefreshView.as_view(), name='token_refresh'),
    # path('logout/', LogoutView.as_view(), name='token_refresh'),
    # path('profile/', ProfileView.as_view(), name='profile'),
]


