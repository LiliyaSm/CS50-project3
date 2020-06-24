from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # path('getEvents/', views.getEvents, name='getEvents'),
    # path("login", views.login_view, name="login"),
    path("cart", views.cart, name="cart"),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'), # POST cart/item
    path('delete_item/', views.delete_item, name='delete_item'), # DELETE cart/item/<id>
    path('update_cart/', views.update_cart, name='update_cart'), # PUT cart/item/<id>
    path('confirm_cart/', views.confirm_cart, name='confirm_cart'), # POST cart/confirm
    path('order_history/', views.order_history, name='order_history'), # GET cart/history
    path('cart/<int:id>/', views.order_detail, name='order_detail'), # GET cart/<id>
    path('cart/<int:id>/repeat', views.order_repeat,
         name ="order_repeat")  # Post cart/<id>/repeate

]
