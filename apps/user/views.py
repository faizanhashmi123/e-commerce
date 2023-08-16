import datetime
from random import randint
import pandas as pd
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView
from application.custom_classes import AjayDatatableView, AdminRequiredMixin, UserRequiredMixin

from .forms import CreateUserForm, EditUserForm, UserSignupForm, EditUserProfileForm

User = get_user_model()


class CreateUserView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'admin/user/form.html'
    success_message = "User created successfully"
    success_url = reverse_lazy('admin-user-list')


class UpdateUserView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = EditUserForm
    template_name = 'admin/user/form.html'
    success_message = "User updated successfully"
    success_url = reverse_lazy('admin-user-list')


class ListUserView(AdminRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/user/list.html'


class ListUserViewJson(AdminRequiredMixin, AjayDatatableView):
    model = User
    columns = ['first_name', 'last_name', 'email', 'is_active', 'actions']
    exclude_from_search_columns = ['actions']
    # extra_search_columns = ['']

    def get_initial_queryset(self):
        return self.model.objects.filter(is_admin=True)

    def render_column(self, row, column):
        if column == 'is_active':
            if row.is_active:
                return '<span class="badge badge-success">Active</span>'
            else:
                return '<span class="badge badge-danger">Inactive</span>'

        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-xs mr-1 text-white">Edit</a>'.format(
                reverse('admin-user-edit', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-xs" data-url={} role="button">Delete</a>'.format(
                reverse('admin-user-delete', kwargs={'pk': row.pk}))
            return edit_action + delete_action
        else:
            return super(ListUserViewJson, self).render_column(row, column)


class DeleteUserView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = User

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)


class ChangeUserPasswordView(AdminRequiredMixin, LoginRequiredMixin, View):
    form_class = SetPasswordForm
    template_name = 'admin/user/change_password.html'
    success_message = 'Password Updated Successfully!'

    def get(self, request, user_id, *args, **kwargs):
        form = self.form_class(get_object_or_404(User, pk=user_id))
        return render(request, self.template_name, {'form': form})

    def post(self, request, user_id, *args, **kwargs):
        form = self.form_class(get_object_or_404(User, pk=user_id), request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
        else:
            return render(request, self.template_name, {'form': form})

        return HttpResponseRedirect(reverse('admin-user-list'))


class ListEmporiaView(AdminRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'admin/user/emporia_list.html'


@method_decorator(never_cache, name='dispatch')
class LandingView(View):
    admin_home_url = 'admin-dashboard'
    user_home_url = 'user-home'
    user_login_url = 'user-login'

    def get(self, request):
        if request.user.is_authenticated and not (request.user.is_superuser or request.user.is_staff):
            return HttpResponseRedirect(reverse(self.user_home_url))
        if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
            return HttpResponseRedirect(reverse(self.admin_home_url))
        return HttpResponseRedirect(reverse(self.user_login_url))



