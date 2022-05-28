from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('api/token/', views.UserTokenView.as_view()),
]
