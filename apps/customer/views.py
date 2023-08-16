from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView
from django.views import View
from django.shortcuts import render, redirect,reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib import messages
from .forms import CreateCustomerUserForm,CreateCustomerForm,EditCustomerUserForm
from application.custom_classes import AjayDatatableView, AdminRequiredMixin, UserRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Customer
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
User = get_user_model()



class CustomerCreateView(CreateView):
    model = Customer
    form_class = CreateCustomerForm
    user_form_class = CreateCustomerUserForm
    template_name = 'customer/register.html'
    success_message = "Customer created successfully"
    success_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        user_form = self.user_form_class()
        return render(request, self.template_name, {'form': form, 'user_form': user_form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        user_form = self.user_form_class(request.POST)
        
        if all([form.is_valid(), user_form.is_valid()]):
            user = user_form.save(commit=False)
            user.type = 'customer'
            user.save()

            email = user_form.cleaned_data['email']
            if Customer.objects.filter(user__email=email).exists():
                return render(request, self.template_name, {'form': form, 'user_form': user_form})

            phone_number = form.cleaned_data['phone_number']
            if Customer.objects.filter(phone_number=phone_number).exists():
                return render(request, self.template_name, {'form': form, 'user_form': user_form})

            customers = form.save(commit=False)
            customers.user = user
            customers.save()

            messages.success(request, self.success_message)
            return redirect(self.success_url)
        else:
            if 'phone_number' in form.errors:
                messages.error(request, "This phone number is already in use.")
            if 'email' in user_form.errors:
                messages.error(request, "This email is already in use.")
            return render(request, self.template_name, {'form': form, 'user_form': user_form})
    


class CustomerLogin(View):
    success_message = 'You have successfully logged in.'
    failure_message = 'Please check credentials.'

    def get(self, request, *args, **kwargs):
        return render(request, 'customer/login.html')

    def post(self, request):
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username,
                            password=password)
        if user is not None:
            login(request, user)
            messages.success(request, self.success_message)
            return HttpResponseRedirect(reverse('website'))
        else:
            messages.error(request, self.failure_message)
            return HttpResponseRedirect(reverse('login'))


class WebisteView(TemplateView):
    template_name = 'customer/index.html'
    
    
class ContactView(TemplateView):
    template_name = 'customer/contact.html'
    
    
class CreateCustomerView(AdminRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'customer/list.html'
    
    
class ListCustomerViewJson(AdminRequiredMixin, AjayDatatableView):
    model = Customer
    columns = ['first_name', 'phone_number', 'user.email','user.is_active', 'actions']
    exclude_from_search_columns = ['actions']
    extra_search_columns = ['first_name','phone_number']

    def get_initial_queryset(self):
        return self.model.objects.all()

    def render_column(self, row, column):
        if column == 'user.is_active':
            if row.user.is_active:
                is_active = False
                _kwargs = {'pk': row.user.id, 'is_active': is_active}
                return '<a href={} ><span class="badge badge-success">Active</span></a>'.format(
                    reverse('change_customer_status', kwargs=_kwargs))
            else:
                is_active = True
                _kwargs = {'pk': row.user.id, 'is_active': is_active}
                return '<a href={} ><span class="badge badge-danger">Inactive</span></a>'.format(
                    reverse('change_customer_status', kwargs=_kwargs))

        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-xs mr-1 text-white">Edit</a>'.format(
                reverse('Customer-user-update', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-xs" data-url={} role="button">Delete</a>'.format(
                reverse('Customer-user-delete', kwargs={'pk': row.pk}))
            # return edit_action + delete_action
        else:
            return super(ListCustomerViewJson, self).render_column(row, column)


class DeleteCustomerView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Customer
    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)


def change_customer_status(request, pk, is_active):
    user = Customer.objects.filter(user__id=pk).first().user
    user.is_active = is_active
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class CustomerUpdateView(AdminRequiredMixin, LoginRequiredMixin,UpdateView):
    model = Customer
    form_class = CreateCustomerForm
    user_form_class = EditCustomerUserForm
    template_name = 'customer/form.html'
    success_message = "Customer updated successfully"
    success_url = reverse_lazy('customer_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(instance=self.object)
        if 'user_form' not in context:
            context['user_form'] = self.user_form_class(instance=self.object.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=self.object)
        user_form = self.user_form_class(request.POST, instance=self.object.user)
        if all([form.is_valid(), user_form.is_valid()]):
            user = user_form.save(commit=False)
            user.type = 'customer'
            user.save()
            customers = form.save(commit=False)
            customers.user = user
            customers.save()
            messages.success(request, self.success_message)
            return redirect(self.success_url)
        else:
            messages.error(request, "Error: This email is already exists")
            return render(request, self.template_name, {'form': form, 'user_form': user_form})






