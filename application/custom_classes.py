from django import http
from django.contrib.auth.mixins import AccessMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db import models
from django.http import Http404

from django.contrib.auth.views import redirect_to_login


class AjayDatatableView(BaseDatatableView):
    extra_search_columns = []
    exclude_from_search_columns = []

    def get_filter_method(self):
        return self.FILTER_ICONTAINS

    def filter_queryset(self, qs):
        columns = self._columns
        if not self.pre_camel_case_notation:
            # get global search value
            search = self._querydict.get('search[value]', None)
            q = Q()
            filter_method = self.get_filter_method()
            for col_no, col in enumerate(self.columns_data):
                # col['data'] - https://datatables.net/reference/option/columns.data
                data_field = col['data']

                try:
                    data_field = int(data_field)
                except ValueError:
                    pass
                if isinstance(data_field, int):
                    column = columns[data_field]  # by index so we need columns definition in self._columns
                else:
                    column = data_field
                if column in self.exclude_from_search_columns:
                    continue
                column = column.replace('.', '__')
                # apply global search to all searchable columns
                if search and col['searchable']:
                    q |= Q(**{'{0}__{1}'.format(column, filter_method): search})

                # column specific filter
                if col['search.value']:
                    qs = qs.filter(**{
                        '{0}__{1}'.format(column, filter_method): col['search.value']})

            columns = self.extra_search_columns
            for column in columns:
                column = column.replace('.', '__')
                if search:
                    search_part = search.split(' ')
                    for part in search_part:
                        q |= Q(**{'{0}__{1}'.format(column, filter_method): part})

            qs = qs.filter(q)
        return qs


class UserRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    login_url = 'user-login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        elif not (request.user.is_superuser or request.user.is_staff):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404


class AdminRequiredMixin(AccessMixin):
    login_url = 'admin-login'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        elif request.user.is_superuser or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        raise Http404


class CorsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if (request.method == "OPTIONS"  and "HTTP_ACCESS_CONTROL_REQUEST_METHOD" in request.META):
            response = http.HttpResponse()
            response["Content-Length"] = "0"
            response["Access-Control-Max-Age"] = 86400
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "DELETE, GET, OPTIONS, PATCH, POST, PUT"
        response["Access-Control-Allow-Headers"] = "accept, accept-encoding, authorization, content-type, dnt, origin, user-agent, x-csrftoken, x-requested-with"
        return response