from django.urls import path
from route.views import (
    RouteInfoView,
    OrderPlaceView,
)


urlpatterns = [
    path('count/', RouteInfoView.as_view(), name='count-route'),
    path('order/', OrderPlaceView.as_view(), name='order-place'),
]
