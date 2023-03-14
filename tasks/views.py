from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import CreateTaskForm
from .models import Task

# Create your views here.

# TODO Ruta principal
def index(request):
    return render(request, 'tasks/index.html', {'title': 'Inicio'})


# TODO Registro de nuevos usuarios usando UserCreationForm para validar y procesar los datos del formulario
def signup(request):
    if request.method == 'GET':
        return render(request, 'tasks/signup.html', {
            'title': 'Registro',
        })
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('tasks:tasks'))
        else:
            errors = form.errors.get('__all__')

            return render(request, 'tasks/signup.html', {
                'form': form,
                'errors': errors,
                'title': 'Registro',
            })


# TODO Registro de nuevos usuarios de la manera mas basica posible
def signup2(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']

        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=username, password=password)
                user.save()
                login(request, user)
                return redirect(reverse('tasks:tasks'))

            except IntegrityError:
                return render(request, 'tasks/signup.html', {
                    'form': UserCreationForm(),
                    'title': 'Registrate',
                    'error': 'El usuario ya existe.'
                })

        return render(request, 'tasks/signup.html', {
            'form': UserCreationForm(),
            'title': 'Registrate',
            'error': 'Las contraseñas no coinciden'
        })
    else:
        return render(request, 'tasks/signup.html', {
            'form': UserCreationForm(),
            'title': 'Registrate',
        })


# TODO Cierre de sesión de usuario
@login_required
def logoutUser(request):
    logout(request)
    return redirect(reverse('tasks:index'))


# TODO Inicio de sesión. Se utiliza get form.get_user() para autenticar al usuario.
def loginUser(request):
    if request.method == 'GET':
        return render(request, 'tasks/login.html', {
            'title': 'Inicio de sesión',
        })
    else:
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('tasks:tasks'))
        else:
            errors = form.errors.get('__all__')

            return render(request, 'tasks/login.html', {
                'form': form,
                'errors': errors,
                'title': 'Inicio de sesión',
            })

#! Alternativa de Inicio de sesión. Se utiliza un form para validar la información de los campos
def loginUser2(request):
    if request.method == 'GET':
        return render(request, 'tasks/login.html', {
            'form': AuthenticationForm(),
            'title': 'Inicio de sesión',
        })
    else:
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(reverse('tasks:tasks'))

        return render(request, 'tasks/login.html', {
            'form': form,
            'title': 'Inicio de sesión',
        })

#! Alternativa de Inicio de sesión. Es la forma mas básica
def loginUser3(request):
    if request.method == 'GET':
        return render(request, 'tasks/login.html', {
            'form': AuthenticationForm(),
            'title': 'Inicio de sesión',
        })
    else:
        username = request.POST['username']
        password = request.POST['password']

        # Validar los campos por medio de authenticate()
        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'tasks/login.html', {
                'form': AuthenticationForm(),
                'title': 'Inicio de sesión',
                'error': 'El usuario o la contraseña son incorrectos',
            })

        login(request, user)
        return redirect(reverse('tasks:tasks'))


# TODO Mostrar las tareas del usuario, provenientes de la base de datos
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks/tasks.html', {
        'tasks': tasks,
        'title': 'Tareas'
    })


# TODO Se muestran las tareas completadas del usuario
@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks/tasks.html', {
        'tasks': tasks,
        'title': 'Tareas completadas',
        'completed': True,
    })

# TODO Agregar una nueva tarea. Esta tarea estará vinculada al usuario que esté en la sesión
@login_required
def tasks_create(request):
    if request.method == 'GET':
        return render(request, 'tasks/createTask.html', {
            'form': CreateTaskForm(),
            'title': 'Agregar tarea',
        })
    else:
        form = CreateTaskForm(data=request.POST)

        if form.is_valid():
            # Esto regresa una instancia de objeto sin guardar, lleno con la informacion que venga en los campos del formulario.
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            return redirect(reverse('tasks:tasksCreate'))
        else:
            errors = form.errors.get('__all__')
            return render(request, 'tasks/createTask.html', {
                'form': form,
                'errors': errors,
                'title': 'Agregar tarea',
            })
        

# TODO Marcar una tarea como completada
@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect(reverse('tasks:tasks'))


# TODO Mostrar los detalles de una tarea en específico y poder modificar sus datos
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'GET':
        form = CreateTaskForm(instance=task)

        return render(request, 'tasks/taskDetail.html', {
            'task': task,
            'form': form,
            'title': 'Detalle',
        })
    else:
        # ? Haciendo el Update cuando se manda a llamar con metodo POST
        form = CreateTaskForm(data=request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect(reverse('tasks:tasks'))
        else:
            errors = form.errors.get('__all__')

            return render(request, 'tasks/taskDetail.html', {
                'task': task,
                'form': form,
                'errors': errors,
                'title': 'Detalle',
            })


# TODO Eliminar una tarea de la base de datos
@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    
    if request.method == 'POST':
        task.delete()
        return redirect(reverse('tasks:tasks'))