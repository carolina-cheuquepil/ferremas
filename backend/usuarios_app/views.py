from django.shortcuts import render, redirect
from django import forms
from usuarios_app.models import Cliente
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages



# 🧾 Formulario de registro
class RegistroForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

    class Meta:
        model = Cliente
        fields = ['nombre', 'correo', 'direccion', 'telefono', 'rut', 'contrasena']

# 🧠 Vista de registro
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            # Paso 1: Guardar los datos del cliente sin comprometer aún la BD
            cliente = form.save(commit=False)

            # Paso 2: Crear el usuario de Django con su correo y contraseña
            user = User.objects.create_user(
                username=cliente.correo,
                password=form.cleaned_data['contrasena']
            )

            # Paso 3: Asociar ese User al cliente
            cliente.usuario = user

            # Paso 4: Eliminar la contraseña almacenada en Cliente si no la usas más
            cliente.contrasena = ''  # Puedes quitar este campo más adelante

            # Paso 5: Guardar finalmente el cliente
            cliente.save()

            # Paso 6: Iniciar sesión automáticamente con ese usuario
            login(request, user)

            # Paso 7: Redirigir o mostrar mensaje de bienvenida
            return render(request, 'bienvenida.html', {'nombre': cliente.nombre})

    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})

# 🧾 Formulario de login
class LoginForm(forms.Form):
    correo = forms.EmailField(label="Correo")
    contrasena = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

# 🧠 Vista de login
def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        correo = form.cleaned_data['correo']
        contrasena = form.cleaned_data['contrasena']

        # Paso 1: Buscar usuario por nombre de usuario (correo)
        usuario = authenticate(request, username=correo, password=contrasena)

        if usuario is not None:
            # Paso 2: Iniciar sesión
            login(request, usuario)

            # Paso 3: Mostrar bienvenida personalizada
            return render(request, 'bienvenida.html', {'nombre': usuario.cliente.nombre})
        else:
            # Paso 4: Mostrar error si no se autenticó
            form.add_error(None, "Credenciales inválidas")

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente 👋")
    return redirect('/productos/lista/')  # Redirige al inicio o donde quieras




