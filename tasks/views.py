from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User,Group,GroupManager,UserManager
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm,AuthUserForm
from .models import Task,AuthUser
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':

        return render(request, 'signup.html', {
            'form': UserCreationForm
        })

    else:

        if request.POST['password1'] == request.POST['password2']:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )

                user.save()
                # login(request, user)
                return redirect('usuarios')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exist'
                })

        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password do not match'
        })


@login_required
def tasks(request):

    # Se traen todos los datos y se filtran por el usuario
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {"tasks": tasks})


@login_required
def usuarios(request):

    usuar = AuthUser.objects.all()
    test = request.user.groups.values_list
    # for groups in request.user.groups.values_list:
    #     for group in groups
    #         if group == 'Administrador'
    #             print(group)
    #         endif
    #     endfor
    # endfor
            
    return render(request, 'usuarios.html', {"usuario": usuar})


@login_required
def modificar_usuario(request, id):

    if request.method == 'GET':

        user = get_object_or_404(AuthUser, pk=id)
        form = AuthUserForm(instance=user)
        return render(request, 'modificar_usuario.html', {
            'task': user,
            'form': form
        })

    else:

        try:
            user = get_object_or_404(AuthUser, pk=id)
            form = AuthUserForm(request.POST, instance=user)
            form.save()
            return redirect('usuarios')
        except ValueError:
            return render(request, 'modificar_usuario.html', {
                'task': user,
                'form': form,
                'error': 'Error en datos'
            })

        # try:
        #     task = get_object_or_404(Task, pk=task_id, user=request.user)
        #     form = TaskForm(request.POST, instance=task)
        #     form.save()
        #     return redirect('tasks')
        # except ValueError:
        #     return render(request, 'task_detail.html', {
        #         'task': task,
        #         'form': form,
        #         'error': 'Error updating task'
        #     })


@login_required
def eliminar_usuario(request, id):
    user = get_object_or_404(AuthUser, pk=id)

    if request.method == 'GET':
        user.delete()
        return redirect('usuarios')


@login_required
def tasks_completed(request):

    # Se traen todos los datos y se filtran por el usuario
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {"tasks": tasks})


@login_required
def create_task(request):

    if request.method == 'GET':

        return render(request, 'create_task.html', {
            'form': TaskForm
        })

    else:

        try:

            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')

        except ValueError:

            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Please provide valid data'
            })


@login_required
def task_detail(request, task_id):

    if request.method == 'GET':

        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })

    else:

        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': 'Error updating task'
            })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):

    if request.method == 'GET':

        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })

    else:

        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:

            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })

        else:
            login(request, user)
            return redirect('home')


# class UserUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
#     model = AuthUser
#     form_class = AuthUserForm
#     template_name = 'modificar_usuario.html'
#     success_url = reverse_lazy('user_user_list')
#     permission_required = 'user.add_user'
#     url_redirect = success_url
    
#     def dispatch(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         return super().dispatch(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             action = request.POST['action']
#             if action == 'edit':
#                 form = self.get_form()
#                 data = form.save()
#             else:
#                 data['error'] = 'No a ingresado nada'
#         except Exception as e:
#             data['error'] = str(e)
            
#         return JsonResponse(data)

@login_required
def prueba(request):

    return render(request, 'prueba.html')