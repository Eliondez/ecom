from django.urls import path, include

from .api import urls

app_name = 'order'

urlpatterns = [
    path('api/', include(urls)),
]

