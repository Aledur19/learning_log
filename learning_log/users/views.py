from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import reverse, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from learning_logs.forms import EditProfileForm

from django.contrib.auth.models import User


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))


def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'users/register.html', context)
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(request, username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            # return redirect('learning_logs:index')
            return HttpResponseRedirect(reverse('learning_logs:index'))

        context = {'form': form}
        return render(request, 'users/register.html', context)


def user_info(request, user_username):
    user = User.objects.get(username=user_username)
    context = {'user': user}
    return render(request, 'users/profile.html', context)


def user_edit(request, user_username):
    user = User.objects.get(username=user_username)

    if request.method != "POST":
        form = EditProfileForm(instance=request.user)
        context = {
            'form': form
        }
        return render(request, 'users/user_edit.html', context)
    else:
        form = EditProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:user_info', args=[request.user]))


def change_password(request):
    if request.method != "POST":
        form = PasswordChangeForm(user=request.user)
        context = {
            'form': form
        }
        return render(request, 'users/change_password.html', context)
    else:
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('users:user_info', args=[request.user]))
        else:
            return HttpResponseRedirect(reverse('users:change_password', args=[request.user]))
