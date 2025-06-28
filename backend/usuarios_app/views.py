from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from usuarios_app.models import Cliente, Usuario
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from forms import UsuarioForm  # Asegúrate de tener el formulario creado

class RegistroForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

    class Meta:
        model = Cliente
        fields = ['nombre', 'correo', 'direccion', 'telefono', 'rut', 'contrasena']

#1. Formulario de login --------------------
#Clientes
class LoginForm(forms.Form):
    correo = forms.EmailField(label="Correo")
    contrasena = forms.CharField(widget=forms.PasswordInput, label="Contraseña")


#------------- Parte 2: Registro de cliente 🤗--------------------
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

            # Paso 7: Redirigir a la lista de productos
            return redirect('/productos/lista/')  
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})



# ------------- Parte 3: Login de cliente 😊--------------------
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
            return redirect('/productos/lista/')  
        else:
            # Paso 4: Mostrar error si no se autenticó
            form.add_error(None, "Credenciales inválidas")

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente 👋")
    return redirect('/productos/lista/')  # Redirige al inicio o donde quieras





# PARTE 1 Empleados--------------------

def lista_usuarios_view(request):
    usuarios = Usuario.objects.all()
    return render(request, 'pagina/empleados.html', {'usuarios': usuarios})




# Editar
def editar_usuario_view(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'pagina/editar_usuario.html', {'form': form})

# Eliminar
def eliminar_usuario_view(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        return redirect('lista_usuarios')
    return render(request, 'pagina/eliminar_usuario.html', {'usuario': usuario})



# Procesa formulario: Frontend 2 TRABAJADORES 


def login_trabajador_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            # Verificar si tiene un perfil de Usuario
            if hasattr(usuario, 'usuario'):
                login(request, usuario)

                if usuario.usuario.cargo == 'Bodeguero':
                    return redirect('sistema_bodega')
                elif usuario.usuario.cargo == 'Vendedor':
                    return redirect('sistema_vendedor')
                else:
                    return redirect('acceso_denegado')
            else:
                return render(request, 'pagina/login_trabajador.html', {
                    'error': 'Este usuario no tiene un perfil asociado en la tabla Usuario.'
                })
        else:
            return render(request, 'pagina/login_trabajador.html', {
                'error': 'Usuario o contraseña incorrectos'
            })

    return render(request, 'pagina/login_trabajador.html')


from django.shortcuts import render, redirect
from pedidos_app.models import Pedido
from pagos_app.models import Pago
from inventario_app.models import HistorialInventario

def sistema_vendedor(request):
    if not request.user.is_authenticated or request.user.usuario.cargo != 'Vendedor':
        return redirect('acceso_denegado')

    pedidos = Pedido.objects.all()
    pagos = Pago.objects.all()
    inventario = HistorialInventario.objects.all()

    return render(request, 'pagina/sistema_vendedor.html', {
        'pedidos': pedidos,
        'pagos': pagos,
        'inventario': inventario,
    })


def crear_usuario_form(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        if form.is_valid():
            # 1. Crear el usuario de Django (auth_user)
            user = User.objects.create_user(username=username, password=password)
            
            # 2. Crear el usuario personalizado y asociar con auth_user
            usuario = form.save(commit=False)
            usuario.user = user
            usuario.save()

            return redirect('lista_usuarios')
        else:
            return render(request, 'pagina/crear_usuario.html', {'form': form, 'error': 'Datos inválidos'})

    else:
        form = UsuarioForm()
    return render(request, 'pagina/crear_usuario.html', {'form': form})



















