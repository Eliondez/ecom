from django.urls import path, include

from .api import urls

app_name = 'gis_meteo'

urlpatterns = [
    path('api/', include(urls)),
]

