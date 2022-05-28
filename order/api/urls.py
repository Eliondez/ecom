from django.urls import path

from . import viewsets as vs

app_name = 'cart_api'

urlpatterns = [
    path('cart_list/', vs.GetCartListView.as_view()),
    path('cart_detail/', vs.GetCartDetailView.as_view()),
    path('adjust_item/', vs.AddToCartView.as_view()),
    path('remove_from_cart/', vs.RemoveFromCartView.as_view()),
    path('clear_cart/', vs.ClearCartView.as_view()),
]

