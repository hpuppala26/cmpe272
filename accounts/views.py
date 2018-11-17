from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate
from accounts.forms import (
    RegistrationForm,
    EditProfileForm
)
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.views.generic import UpdateView
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


# Create your views here.
@login_required(login_url="/accounts/login")
def home(request):
    return redirect('articles:list')




def signup_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:details')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})




def signup_detailsview(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if profile_form.is_valid():
            # picture = profile_form.cleaned_data.get('picture')
            # userprofile.picture = picture
            profile_form.save()
            return redirect('articles:list')
        else:
            messages.error(request, ('Please correct the error below'))
    else:
        profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'accounts/details.html', {'profile_form': profile_form})






def login_view(request):
     # if request.user:
     #     return redirect('articles:list')
     # else:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('articles:list')
        else:
            form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})




def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'accounts/logout.html')




@login_required(login_url="/accounts/login")
def view_profile(request, username):
    user = User.objects.get(username=username)
    editable = False
    if request.user.is_authenticated and request.user == user:
        editable = True

    args = {'user':user, 'editable':editable}
    return render(request, 'accounts/profile.html', args)



# @login_required(login_url="/accounts/login")
# def view_other(request, username):
#     user_2 = request.user
#     user = User.objects.get(username=username)
#     args = {'user':user, 'user_2':user_2}
#     return render(request, 'accounts/profile.html', args)






@login_required(login_url="/accounts/login")
def edit_profile(request, username):
    user = User.objects.get(username=username)
    if request.user.is_authenticated and request.user == user:
        if request.method == 'POST':
            user_form = EditProfileForm(request.POST, instance=request.user)
            profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, ('Your profile was successfully updated!'))
                return redirect(reverse('accounts:profile', args=[request.user]))
            else:
                messages.error(request, ('Please correct the error below.'))
        else:
            user_form = EditProfileForm(instance=request.user)
            profile_form = UserProfileForm(instance=request.user.userprofile)
        return render(request, 'accounts/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})



@login_required(login_url="/accounts/login")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/profile')
        else:
            return redirect('/accounts/change-password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)




def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.userprofile.email_confirmed = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
