#Paso 1: Fronend
from django import forms
from usuarios_app.models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'direccion', 'telefono', 'cargo', 'rut']
