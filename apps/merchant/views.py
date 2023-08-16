from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import  HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from application.custom_classes import AjayDatatableView, AdminRequiredMixin, UserRequiredMixin
from .forms import *
from .models import *
User = get_user_model()


class CreateMerchantView(CreateView):
    model = Merchant
    form_class = CreateMerchantForm
    user_form_class = CustomUserCreationForm
    template_name = 'merchant/register.html'
    success_message = "Merchant created successfully"
    success_url = reverse_lazy('login')
    

    def get(self, request):
        form = self.form_class()
        user_form = self.user_form_class()
        return render(request, self.template_name, {'form': form, 'user_form': user_form})


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user_form = self.user_form_class(request.POST)
        
        if all([form.is_valid(), user_form.is_valid()]):
            user = user_form.save(commit=False)
            user.type = 'merchant'
            user.save()
            
            email = user_form.cleaned_data['email']
            if Merchant.objects.filter(user__email=email).exists():
                return render(request, self.template_name, {'form': form, 'user_form': user_form})
            
            phone_number = form.cleaned_data['phone_number']
            if Merchant.objects.filter(phone_number=phone_number).exists():
                return render(request, self.template_name, {'form': form, 'user_form': user_form})

            
            merchant = form.save(commit=False)
            merchant.user = user
            merchant.save()
            
            messages.success(request, self.success_message)
            return redirect(self.success_url)
        else:
            if 'phone_number' in form.errors:
                messages.error(request, "This phone number is already in use.")
            if 'email' in user_form.errors:
                messages.error(request, "This email is already in use.")
            return render(request, self.template_name, {'form': form, 'user_form': user_form})
        


class MerchantLogin(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/login.html')

    def post(self, request):
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username,
                            password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'user login succesfully')
            return HttpResponseRedirect(reverse('website'))
        else:
            messages.error(request, 'please valid enter deatils')
            return HttpResponseRedirect(reverse('login'))


class ListMerchantView(AdminRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'merchant/list.html'


class ListMerchantViewJson(AdminRequiredMixin, AjayDatatableView):
    model = Merchant
    columns = ['user.first_name', 'user.email', 'phone_number', 'user.is_active', 'actions']
    exclude_from_search_columns = ['actions']
    extra_search_columns = ['user.first_name', 'user.email','phone_number']

    def get_initial_queryset(self):
        return self.model.objects.all()

    def render_column(self, row, column):
        if column == 'user.is_active':
            if row.user.is_active:
                is_active = False
                status = {'pk': row.user.id, 'is_active': is_active}
                return '<a href={} ><span class="badge badge-success">Active</span></a>'.format(
                    reverse('change-merchant-status', kwargs=status))
            else:
                is_active = True
                status = {'pk': row.user.id, 'is_active': is_active}
                return '<a href={} ><span class="badge badge-danger">Inactive</span></a>'.format(
                    reverse('change-merchant-status', kwargs=status))
                
        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-xs mr-1 text-white">Edit</a>'.format(
                reverse('merchant-update', kwargs={'pk': row.pk}))
            
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-xs " data-url={} role="button">Delete</a>'.format(
                reverse('merchant-delete', kwargs={'pk': row.pk}))
            return edit_action + delete_action
        
        else:
            return super(ListMerchantViewJson, self).render_column(row, column)
        
        
        
def Change_Merchant_Status(request, pk, is_active):
    user = Merchant.objects.filter(user__id=pk).first().user
    user.is_active = is_active
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DeleteMerchantView(LoginRequiredMixin, DeleteView):
    model = Merchant
    success_message = 'Merchant deleted Successfully.'
    success_url = reverse_lazy('merchant-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteMerchantView, self).delete(request, *args, **kwargs)


class UpdateMerchantView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Merchant
    form_class = EditMerchantForm
    user_form_class = EditMerchantUserForm
    template_name = 'merchant/form.html'
    success_message = "Merchant updated successfully"
    success_url = reverse_lazy('merchant-list')
    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super(UpdateMerchantView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET, self.request.FILES, instance=self.object)
        if 'user_form' not in context:
            context['user_form'] = self.user_form_class(instance=self.object.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, request.FILES, instance=self.object)
        user_form = self.user_form_class(request.POST, instance=self.object.user)

        if all([form.is_valid(), user_form.is_valid()]):
            merchant = form.save(commit=False)
            merchant.save()
            user_form.save()
            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(self.success_url)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, user_form=user_form))







