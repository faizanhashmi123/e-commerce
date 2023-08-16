from django.urls import path
from .views import ListCustomerSupportView,CreateCustomerSupportView,ListCustomerSupportJson,UpdateCustomerSupportView,DeleteCustomerSupportView

urlpatterns = [
    path('customersupport/list/', ListCustomerSupportView.as_view(), name='customersupport-list'),
    path('customersupport_create/list/', CreateCustomerSupportView.as_view(), name='customersupport-create'),
    path('customersupport_create/ajx/list/', ListCustomerSupportJson.as_view(), name='customersupport-ajax-list'),
    path('customersupport_create/update/<int:pk>/', UpdateCustomerSupportView.as_view(), name='update-customersupport'),
    path('customersupport_create/delete/<int:pk>', DeleteCustomerSupportView.as_view(), name='delete-CustomerSupport'),



]