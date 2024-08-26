from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

# modulo para manejar errores de integridad de la base de datos
from django.db import IntegrityError

# formulario de creacion de usuarios
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# modelo de usuario
from django.contrib.auth.models import User

# para crear la cookie
from django.contrib.auth import login, logout, authenticate

# importo mis formularios
from .forms import TaskForm

# mis modelos
from .models import Task

# para proteger rutas
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    return render(request, 'home.html')


def signUp(request):

    # Si la solicitud se realiza mediante el método GET, se intenta servir la interfaz solicitada.
    # Si la solicitud se realiza mediante el método POST, se procesa la información enviada.
    if request.method == 'GET':
        # print('Enviando formulario')

        return render(request, 'signup.html', {
            # podemos enviar el formulario, o crear uno propio, pero debe tener los names que maneja django
            'form': UserCreationForm()
        })

    else:
        # print('Obteniendo datos')
        print(request.POST)

        if (request.POST["password1"] == request.POST["password2"]) and len(request.POST["password1"]) >= 6:
            try:
                # creamos y guardamos el usuario
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"])
                user.save()

                # guardamos la cookie, esto genera la sesionId (auntenticacion)
                login(request, user)

                # return HttpResponse('User created successfully')

                return redirect('tasks')

            except IntegrityError:
                return HttpResponse('Username already exists')

            except Exception as e:
                # Capturar el tipo de error y el mensaje
                error_type = type(e).__name__
                error_message = str(e)
                print(f"Error: {error_type} - {error_message}")

                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'error': f"Error: {error_type} - {error_message}",
                    'miCustomError': "Username already exists"
                })

        # return HttpResponse('Password do not match')

    return render(request, 'signup.html', {
        'form': UserCreationForm(),
        'myCustomError': "Password do not match"
    })


@login_required  # con esto decimos que no cualquiera puede acceder
def tasks(request):
    tasks = Task.objects.all()
    # tareas del usuario actual, y solo las que la fecha de completado esten en null, es decir no completadas
    tasks = Task.objects.filter(user=request.user, dateCompleted__isnull=True)

    return render(request, 'tasks.html', {
        "tasks": tasks
    })


@login_required
def createTask(request):

    if request.method == "GET":
        return render(request, 'create_task.html', {
            "form": TaskForm
        })

    else:
        # print(request.POST)

        try:
            form = TaskForm(request.POST)  # genera el formulario (HTML)
            # print(form)
            # el commit=False es para no guardarlo en base de datos, es para hacer pruebas
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            print(new_task)

            return redirect("tasks")

        except ValueError:
            return render(request, 'create_task.html', {
                "form": TaskForm,
                "error": "Please provide valid data"
            })


@login_required
def taskDetail(request, task_id):

    if request.method == "GET":
        # task = Task.objects.get(id=task_id)
        # obtengo solo las tareas del usuario actual
        task = get_object_or_404(Task, id=task_id, user=request.user)
        # obtengo el formulario y lo rellenamos con esa tarea
        form = TaskForm(instance=task)

        return render(request, 'task_detail.html', {
            "task": task,
            "form": form
        })
    else:
        try:
            # print(request.POST)
            # actualizacion de la tarea
            task = get_object_or_404(Task, id=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect("tasks")

        except ValueError:
            return render(request, 'task_detail.html', {
                "task": task,
                "form": form,
                "error": "Error updating task"
            })


@login_required
def completeTask(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        task.dateCompleted = timezone.now()
        task.save()
        return redirect("tasks")


@login_required
def deleteTask(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        task.delete()
        return redirect("tasks")


@login_required
def tasksCompleted(request):

    tasks = Task.objects.filter(
        # ordenadas desde su fecha de completado
        user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')

    return render(request, 'tasks.html', {
        "tasks": tasks
    })

    # no la llamo logout porque chocaria con el logout de django


@login_required
def signOut(request):

    logout(request)

    return redirect('home')


def signIn(request):

    if request.method == "GET":
        return render(request, 'signin.html', {
            'form': AuthenticationForm()
        })

    else:
        print(request.POST)

        user = authenticate(
            request, username=request.POST["username"], password=request.POST["password"])

        if user is None:

            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                "error": "Username or password is incorrect"
            })
        else:

            # guardamos la sesion
            login(request, user)

            return redirect("tasks")
