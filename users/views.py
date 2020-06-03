from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from users.forms import UserRegistrationForm
# Create your views here.


def registration(request):
    if request.method == 'POST':

        # map the submitted form to the UserRegistrationForm
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            # log in the user immediately with given name
            username = form.cleaned_data.get('username')
            login(request, user)
            raw_password = form.cleaned_data.get('password1')
            user = uthenticate(username=username, password=raw_password)
            return redirect('index')
            
    # GET Request
    form = UserRegistrationForm()
    return render(request=request,
                  template_name="users/registration.html",
                  context={"form": form})


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
        return render(request, "users/login.html", {"message": "Invalid credentials."})


def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out."})
