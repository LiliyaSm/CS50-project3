from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from users.forms import UserRegistrationForm


def registration(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':

        # map the submitted form to the UserRegistrationForm
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            # log in the user immediately with given name
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')

        else:
            return render(request=request,
                          template_name="users/registration.html",
                          context={"form": form})
            
    # GET Request
    form = UserRegistrationForm()
    return render(request=request,
                  template_name="users/registration.html",
                  context={"form": form})



