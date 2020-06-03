from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    # path('registration', include('django_registration.backends.one_step.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
]
