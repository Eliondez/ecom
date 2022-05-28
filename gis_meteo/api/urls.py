from django.urls import path

from . import viewsets as vs

app_name = 'gis_meteo_api'

urlpatterns = [
    path('get_last/', vs.GetLastView.as_view()),
    path('test/', vs.TestView.as_view()),
]

