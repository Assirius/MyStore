from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout

from users import forms
from products import models


class Profile(LoginRequiredMixin, View):

    def get(self, request):
        form = forms.UserProfileForm(instance=request.user)
        baskets = models.Basket.objects.filter(user=request.user)
        total_quantity = sum(basket.quantity for basket in baskets)
        total_sum = sum(basket.sum() for basket in baskets)

        context = {
            'form': form,
            'baskets': baskets,
            'total_quantity': total_quantity,
            'total_sum': total_sum
        }
        return render(request, template_name='users/profile.html', context=context)

    def post(self, request):
        form = forms.UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()

            return redirect('users:profile')

        else:
            return render(request, template_name='users/profile.html', context={'form': form})


class Registration(View):

    def get(self, request):
        form = forms.UserRegistrationForm()

        return render(request, template_name='users/register.html', context={'form': form})

    def post(self, request):
        form = forms.UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')

            return redirect('users:login')

        else:
            return render(request, template_name='users/register.html', context={'form': form})


class Login(View):

    def get(self, request):
        form = forms.UserLoginForm()

        return render(request, template_name='users/login.html', context={'form': form})

    def post(self, request):
        form = forms.UserLoginForm(data=request.POST)

        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user.is_active:
                login(request, user)
                return redirect('products:products')
        else:
            return render(request, template_name='users/login.html', context={'form': form})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('users:login')
