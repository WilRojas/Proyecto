from django import forms
from .models import Task,AuthUser


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['tittle', 'description', 'important']
        widgets = {
            'tittle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a tittle'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a description'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'})
        }

generos= [
    (1,'Administrador'),
    (2,'Empleado'),
    (3,'Cliente')
    ]


class AuthUserForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ['username', 'first_name', 'last_name','email','user_type','is_active','password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a first_name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a last_name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a email'}),
            'user_type': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
            'password': forms.PasswordInput(),
        }
        

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