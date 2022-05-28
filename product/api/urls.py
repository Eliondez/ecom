from django.urls import path, include

from rest_framework import routers
from .viewsets import ProductViewset

app_name = 'product_api'

router = routers.DefaultRouter()
router.register(r'', ProductViewset)

urlpatterns = [
    path('catalog/', include(router.urls)),
]

