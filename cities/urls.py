from django.urls import path

from cities.views import CityListView, CityDetailView, CityTemperatureView, StatsView


urlpatterns = [
    path('city/', CityListView.as_view(), name='city'),
    path('city/<uuid:pk>/', CityDetailView.as_view(), name='city-detail'),
    path('city/<uuid:pk>/setTemperature/', CityTemperatureView.as_view(), name='set-temperature'),
    path('stats/', StatsView.as_view(), name='stats'),
]
