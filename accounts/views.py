import datetime
from django.db.models.fields import files
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, Dues, UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
import random
# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

reg_num = random.randint(11111, 29999)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            reg_number = reg_num
            # reg_number=form.cleaned_data['reg_number']
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password, reg_number=reg_number)
            user.phone_number = phone_number,
            user.save()
            
            
            UserProfile.objects.create(
                user=user,
                email=user.email)
            
            # profile.objects.create(
            #     user=user,
            #     email=user.email)
            # profile.save()
            
            
            # full_name = user.first_name + ' ' + user.last_name

            # user account activation
            current_site = get_current_site(request)
            mail_subject = 'Please, Verify Your Email'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Registration initiated, Check your email for activation link')
            return redirect('/accounts/login/?command=verification&email='+email)

    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            # messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials!')
            return redirect('login')
    return render(request, 'accounts/login.html', )


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out successfully!')
    return redirect('login', )


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Congratulations! Your account is activated. You can now longin')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


@login_required(login_url='login')
def profile(request):
    profile = UserProfile.objects.filter(
        user=request.user)

    context = {
        'profile': profile
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user.pk)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile update successful')
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='login')
def dues(request):
    dues = Dues.objects.filter(
        account_holder=request.user)

    context = {
        'dues': dues
    }
    return render(request, 'accounts/dues.html', context)


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(
                request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link is expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()

                auth.logout(request)
                messages.success(
                    request, 'Your password has been updated successfully')
                return redirect('login')
            else:
                messages.error(request, 'Invalid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Your new password does not match')
            return redirect('change_password')

    return render(request, 'accounts/change_password.html')
