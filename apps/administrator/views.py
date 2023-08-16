import datetime
from random import randint

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.views.decorators.cache import never_cache
# importing plan
from django.contrib.auth import get_user_model
import pandas as pd
from application.custom_classes import AdminRequiredMixin

User = get_user_model()
from django.http import HttpResponseRedirect


@method_decorator(never_cache, name='dispatch')
class AdminLoginView(View):
    template_name = 'administrator/login.html'
    success_url = 'admin-dashboard'
    login_url = 'admin-login'
    success_message = 'You have successfully logged in.'
    failure_message = 'Please check credentials.'

    def get(self, request):
        if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
            return HttpResponseRedirect(reverse(self.success_url))
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username,
                            password=password)
        if user and (user.is_superuser or user.is_staff):
            login(request, user)
            messages.success(request, self.success_message)
            return HttpResponseRedirect(reverse(self.success_url))
        else:
            messages.error(request, self.failure_message)
            return HttpResponseRedirect(reverse(self.login_url))


class AdminLogoutView(AdminRequiredMixin, LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have successfully logged out.')
        return redirect('admin-login')


class AdminChangePasswordView(AdminRequiredMixin, LoginRequiredMixin, View):
    template_name = 'administrator/change_password.html'

    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password has been successfully updated!')
        else:
            messages.error(request, 'Error occured while changing password, please enter a proper password.')
            return render(request, self.template_name, {'form': form})
        return redirect('admin-dashboard')


class AdminDashboardView(AdminRequiredMixin, LoginRequiredMixin, View):

    def get(self, request):
        users_count = User.objects.filter(is_staff=False).count()

        # emporia usage data
        now = datetime.datetime.now()
        data_list = []
        label = []

        context = {
                    'users_count': users_count,
                    'label': label,
                   }
        return render(request, 'administrator/dashboard.html', context)

