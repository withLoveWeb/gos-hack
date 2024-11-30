from django.urls import path

from captain.views import (
    RegisterCaptainView,
    CaptainAuthView,
    CaptainLogoutView,
    CaptainProfileView,
    CaptainTokenRefreshView
)


urlpatterns = [
    path('register/', RegisterCaptainView.as_view(), name='registercap'),
    path('auth/', CaptainAuthView.as_view(), name='logincap'),
    path('auth/refresh/', CaptainTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', CaptainLogoutView.as_view(), name='token_refresh'),
    path('profile/', CaptainProfileView.as_view(), name='profile'),
]


