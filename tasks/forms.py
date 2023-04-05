from django import forms
from .models import Usuario
# from .models import Task
# from .models import Task,AuthUser

# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ['tittle', 'description', 'important']
#         widgets = {
#             'tittle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a tittle'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a description'}),
#             'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'})
#         }

# generos= [
#     (1,'Administrador'),
#     (2,'Empleado'),
#     (3,'Cliente')
#     ]


# class AuthUserForm(forms.ModelForm):
#     class Meta:
#         model = AuthUser
#         fields = ['username', 'first_name', 'last_name','email','user_type','is_active','password']
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a username'}),
#             'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a first_name'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a last_name'}),
#             'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a email'}),
#             'user_type': forms.TextInput(attrs={'class': 'form-control'}),
#             'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
#             'password': forms.PasswordInput(),
#         }


# class AuthUserForm(forms.ModelForm):
#     class Meta:
#         model = AuthUser
#         fields = ['username', 'first_name', 'last_name','email','user_type','is_active']
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a username'}),
#             'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a first_name'}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a last_name'}),
#             'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a email'}),
#             # 'user_type': forms.Select(attrs={'class': 'form-control'}, choices=generos),
#             'user_type': forms.TextInput(attrs={'class': 'form-control'}),
#             'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
#             # 'password': forms.PasswordInput(render_value=True, attrs={'placeholder': 'ingrese la contraseña'})
#         }

class FormularioUsuario(forms.ModelForm):

    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la contraseña...',
            'id': 'password1',
            'required': 'required',
        }
    ))

    password2 = forms.CharField(label='Contraseña de confirmación', widget= forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese nuevamente la contraseña...',
            'id': 'password2',
            'required': 'required',
        }
    ))
    
    class Meta:
        model = Usuario
        fields = ('email','username','nombres','apellidos','tipo_usuario')
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Correo Electronico',
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su nombre',
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su usuario',
                }
            ),
            'tipo_usuario': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese su tipo de usuario',
                }
            )
        }
        
    def clean_password2(self):
        
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Contraseñas no coinciden!')
        return password2
    
    def clean_tipo_usuario(self):
        
        tipo_usuario = self.cleaned_data.get('tipo_usuario')
        ListaTipoUsuario = ['Administrador', 'Empleado', 'Cliente']
        
        if tipo_usuario not in ListaTipoUsuario:
            raise forms.ValidationError('Tipo de Usuario no valido!')
        return tipo_usuario
    
    def save(self,commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
        return user