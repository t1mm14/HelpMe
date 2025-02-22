from django.urls import path
from .views import (
    AdvertisementListView,
    AdvertisementDetailView,
    AdvertisementCreateView,
    ResponseCreateView,
    ResponseListView,
    ResponseAcceptView,
    ResponseDeleteView
)

urlpatterns = [
    path('', AdvertisementListView.as_view(), name='advertisement_list'),
    path('advertisement/create/', AdvertisementCreateView.as_view(), name='advertisement_create'),
    path('advertisement/<int:pk>/', AdvertisementDetailView.as_view(), name='advertisement_detail'),
    path('advertisement/<int:pk>/respond/', ResponseCreateView.as_view(), name='response_create'),
    path('responses/', ResponseListView.as_view(), name='response_list'),
    path('response/<int:pk>/accept/', ResponseAcceptView.as_view(), name='response_accept'),
    path('response/<int:pk>/delete/', ResponseDeleteView.as_view(), name='response_delete'),
] 