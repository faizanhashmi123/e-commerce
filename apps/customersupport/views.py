from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView
from application.custom_classes import AjayDatatableView, AdminRequiredMixin, UserRequiredMixin
from .forms import SupportTicketForm
from .models import *

class CreateCustomerSupportView(View):
    template_name = 'customer_support/form.html'
    success_message = "customer_support created successfully"
    success_url = 'customersupport-list'

    def get(self, request):
        form = SupportTicketForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            customer_support = form.save(commit=False)
            customer_support.user = request.user
            customer_support.save()
            messages.success(request, self.success_message)
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'form': form})


class ListCustomerSupportView(AdminRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'customer_support/list.html'



class ListCustomerSupportJson(AdminRequiredMixin, AjayDatatableView):
    model = SupportTicket
    columns = ['subject', 'description', 'status','actions']
    exclude_from_search_columns = ['actions']
    extra_search_columns = ['subject','description']

    def get_initial_queryset(self):
        return self.model.objects.all()

    def render_column(self, row, column):
        if column == 'is_active':
            if row.is_active:
                return '<span class="badge badge-success">Active</span>'
            else:
                return '<span class="badge badge-danger">Inactive</span>'
        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-xs mr-1 text-white">Edit</a>'.format(
                reverse('update-customersupport', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-xs" data-url={} role="button">Delete</a>'.format(
                reverse('delete-CustomerSupport', kwargs={'pk': row.pk}))
            return edit_action + delete_action
        else:
            return super(ListCustomerSupportJson, self).render_column(row, column)

class UpdateCustomerSupportView(AdminRequiredMixin, LoginRequiredMixin,UpdateView):
    model = SupportTicket
    template_name = 'customer_support/form.html'
    form_class = SupportTicketForm
    success_message = "Customer support updated successfully"
    success_url = 'customersupport-list'

    def get_object(self, queryset=None):
        ticket_id = self.kwargs.get('pk')
        return get_object_or_404(SupportTicket, pk=ticket_id)

    def form_valid(self, form):
        customer_support = form.save(commit=False)
        customer_support.user = self.request.user
        customer_support.save()
        messages.success(self.request, self.success_message)
        return redirect(self.success_url)


class DeleteCustomerSupportView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = SupportTicket
    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)
