from django.shortcuts import redirect, render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TodoForm, UserForm, SignUserForm, SettingForm
from .models import Todo, Setting
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    form = SignUserForm()
    if request.method == 'POST':
        form = SignUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
    return render(request, 'todo/signupuser.html', {'form': form})

def loginuser(request):
    if request.GET.get('next'):
        next_page = request.GET['next']
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm, 'error':'username or password didn\'t match'})
        else:
            login(request, user)
            if request.GET.get('next'):
                return HttpResponseRedirect(next_page)
            return redirect('home')


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def profile(request, user_id):
    user = User.objects.get(id=user_id)
    return render (request, 'todo/profile.html', {'user':user})
    
@login_required
def settings(request, user_id):
    user = request.user
    user_form = UserForm(instance=user)
    setting_form = SettingForm(instance=user.setting)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        setting_form = SettingForm(request.POST, request.FILES, instance=user.setting)
        if user_form.is_valid() and setting_form.is_valid():
            user_form.save()
            setting_form.save()
            return  redirect('profile', user_id=user.id)
    context = {'user_form': user_form, 'setting':setting_form}
    return render(request, 'todo/settings.html', context)

def current(request):
    todos = Todo.objects.filter(user=request.user)
    return render(request, 'todo/current.html', {'todos': todos})

@login_required
def viewtodo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error':'Bad info'})

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos':todos})


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        form = TodoForm(request.POST)
        newtodo = form.save(commit=False)
        newtodo.user = request.user
        newtodo.save()
        return redirect('currenttodos')



@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def delete_account(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('home')
    return render(request, 'todo/delete_account.html')