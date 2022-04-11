from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm


# Create your views here.
# * Inicio de sesion
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    # Validar si el request es POST
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Usuario o contraseña incorrectos'
        else:
            msg = 'Error al validar formulario'

    return render(request, "registration/login.html", {"form": form, "msg": msg})


# * Registro de usuario
def register_user(request):
    msg = None
    success = False
    # Validar si el request es POST
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            msg = 'User created - please <a href="/login">login</a>.'
            success = True
            return redirect('/')
        else:
            msg = 'Error al validar formulario'
    else:
        form = SignUpForm()

    return render(request, "registration/register.html", {"form": form, "msg": msg, "success": success})
