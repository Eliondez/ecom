from django.urls import path, include

from .api import urls

app_name = 'product'

urlpatterns = [
    path('api/', include(urls)),
]

