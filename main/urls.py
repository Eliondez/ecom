from django.contrib import admin
from django.urls import path, include

from .views import index_view
from simulation.views import simulation_view
from gis_meteo import views as gm_views


app_name = 'main'

urlpatterns = [
    # path('api/', include('api.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('product/', include('product.urls', namespace='product')),
    path('gis_meteo/', include('gis_meteo.urls', namespace='gis_meteo')),
    path('order/', include('order.urls', namespace='order')),
    path('user/', include('user.urls')),
    path('admin/', admin.site.urls),
    path('', index_view),
    path('gis_meteo', gm_views.index),
    path('simulation', simulation_view),

]
