from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .forms import UserRegisterForm

# --- REGISTRO ---
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            user.username = email.split('@')[0]
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registro exitoso. Ahora puedes iniciar sesión.")
            return redirect('login')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


# --- LOGIN CON CORREO ---
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            messages.error(request, "Correo no registrado.")
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # ajusta si no tienes aún esa vista
        else:
            messages.error(request, "Contraseña incorrecta.")
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    """Cerrar sesión del usuario y redirigir al login."""
    logout(request)
    messages.info(request, "Has cerrado sesión.")
    return redirect('login')
