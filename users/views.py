from django.shortcuts import render, redirect
from users.forms import UserRegistrationForm
from django.contrib.auth import logout, authenticate, login

# Create your views here.


def registration(request):
    if request.method == 'POST':

        # map the submitted form to the UserCreationForm
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # log in the user immediately with given name
            username = form.cleaned_data.get('username')
            login(request, user)

            return redirect('index')
            
    # GET Request
    form = UserRegistrationForm()
    return render(request=request,
                  template_name="users/registration.html",
                  context={"form": form})


# def registration(request):
#     """ a new user registration """
#     username = request.POST["username"]
#     password = request.POST["password"]
#     email = request.POST["email"]
#     first_name = request.POST["first_name"]
#     last_name = request.POST["last_name"]
#     return render(request, "menu/registration.html", {"message": None})
