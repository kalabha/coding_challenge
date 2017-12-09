import pdb

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth import logout as auth_logout

from custom_auth.forms import SignUpForm
from custom_auth.models import Otp

CustomUser = get_user_model()


@login_required()
def index(request):
    return render(request, 'custom_auth/index.html')


def sign_up(request):
    form = SignUpForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            otp = Otp.objects.create(user=user)
            otp.send_otp_as_mail()
            messages.add_message(request, messages.SUCCESS, 'OTP Send to Your registered mail id')
            context = {
                'email': user.email,
                'form_url': reverse("custom_auth:verify_otp")
            }
            return render(request, 'custom_auth/verify_otp.html', context)

    context = {
        'form': form,
        'form_url': reverse("custom_auth:sign_up"),

    }

    return render(request, 'custom_auth/sign_up.html', context)


def get_otp(code, email):
    try:
        otp = Otp.objects.get(user__email=email, code=code)
        return otp

    except (TypeError, Otp.DoesNotExist, FieldError):
        return None


@login_required
def userlogout(request):
    auth_logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logged Out!!')
    return HttpResponseRedirect(reverse("custom_auth:login"))


def userlogin(request):
    if request.POST.get('email'):
        try:
            user = CustomUser.objects.get(email=request.POST.get('email'))
            otp = Otp.objects.create(user=user)
            otp.send_otp_as_mail()
            messages.add_message(request, messages.SUCCESS, "OTP send to registered email id.")
            context = {
                'email': user.email,
                'form_url': reverse("custom_auth:verify_otp")
            }
            return render(request, 'custom_auth/verify_otp.html', context)
        except CustomUser.DoesNotExist:
            messages.add_message(request, messages.WARNING, "Email id doesn't exist!")
            return HttpResponseRedirect(reverse('custom_auth:sign_up'))
    return render(request, "custom_auth/request_otp.html")


def verify_otp(request):
    if request.method == "POST" and request.POST.get('code'):
        otp = get_otp(code=request.POST.get('code'), email=request.POST.get('email1'))
        if otp:
            if otp.is_active():
                if not otp.user.is_active:
                    otp.user.make_user_active()
                auth_login(request, otp.user)
                messages.add_message(request, messages.SUCCESS, 'Welcome!!')
            else:
                messages.add_message(request, messages.WARNING, 'OTP Expired. Try to login again!!')
            otp.delete()
            return HttpResponseRedirect('/')

        messages.add_message(request, messages.WARNING, 'OTP is Incorrect!')
        # return HttpResponseRedirect(reverse('custom_auth:verify_otp'))
    context = {

        'form_url': reverse("custom_auth:verify_otp"),
        'email': request.POST.get('email', False)

    }

    return render(request, 'custom_auth/verify_otp.html', context)
