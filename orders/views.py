from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.shortcuts import redirect
from .models import Item

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    context = {
        "user": request.user,
        "items": Item.objects.all()
    }

    return render(request, "menu/index.html", context)




