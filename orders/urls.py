from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # path('getEvents/', views.getEvents, name='getEvents'),
    # path("login", views.login_view, name="login"),
    path("cart", views.cart, name="cart"),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('delete_item/', views.delete_item, name='delete_item'),
    path('update_cart/', views.update_cart, name='update_cart'),
]
