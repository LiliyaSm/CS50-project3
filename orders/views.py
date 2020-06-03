from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Item

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, "menu/login.html", {"message": None})
    context = {
        "user": request.user,
        "items": Item.objects.all()
    }

    return render(request, "menu/index.html", context)

    # return HttpResponse("Project 3: TODO")


def login_view(request):

    try:
        username = request.POST["username"]
        password = request.POST["password"]
    except:
        pass
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "menu/login.html", {"message": "Invalid credentials."})


def logout_view(request):
    logout(request)
    return render(request, "menu/login.html", {"message": "Logged out."})

