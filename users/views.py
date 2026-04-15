import random
from django.contrib import messages
from django.contrib.auth.middleware import LoginRequiredMiddleware
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from eskiz_sms import EskizSMS

from cities_light.models import Country
from .models import User

email = "tursunovotabekkuva@gmail.com"
password = "zXPcPjJenT6tQXLKZ89BQWhzN7abYxRTE8JtqZwt"
eskiz = EskizSMS(email=email, password=password)


class RegisterView(View):
    def get(self, request):
        countries = Country.objects.all()

        context = {
            'countries': countries
        }
        return render(request, 'register.html', context)

    def post(self, request):
        if User.objects.filter(phone=request.POST.get('phone')).exists():
            messages.error(request, "Telefon raqamda hisob allaqachon mavjud!")
            return render(request, 'register.html')
        elif request.POST.get('password') != request.POST.get('repeat_password'):
            messages.error(request, "Parollar mos emas!")
            return render(request, 'register.html')
        else:
            user = User.objects.create_user(
                username=request.POST.get('phone'),
                password=request.POST.get('password'),
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                phone=request.POST.get('phone'),
                gender=request.POST.get('gender'),
                country=get_object_or_404(Country, pk=request.POST.get('country_id')),
                city=request.POST.get('city'),
            )

            confirmation_code = random.randint(100000, 999999)
            user.confirmation_code = f"{confirmation_code}"
            print(confirmation_code)
            user.save()

            login(request, user)

            eskiz.send_sms(user.phone, f"Bu Eskiz dan test")

            return redirect('register-confirm')


class RegisterConfirmView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'register-confirm.html')

    def post(self, request):
        if request.POST.get('confirmation_code') == request.user.confirmation_code:
            user = request.user
            user.confirmed = True
            user.save()
            return redirect('home')
        messages.error(request, "Notog'ri kod kiritildi!")
        return self.get(request)


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        pass


def logout_view(request):
    logout(request)
    return redirect('register')
