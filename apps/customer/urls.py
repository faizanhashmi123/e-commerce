from django.urls import path
from .views import *

urlpatterns = [
    path('register/', CustomerCreateView.as_view(), name='register_customer'),
    path('login/', CustomerLogin.as_view(), name='login'),
    path('website/', WebisteView.as_view(), name='website'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('customer-list/', CreateCustomerView.as_view(), name='customer_list'),
    path('Customer/list/ajax', ListCustomerViewJson.as_view(), name='Customer-list-ajax'),
    path('Customer/delete/<int:pk>', DeleteCustomerView.as_view(), name='Customer-user-delete'),
    path('Customer/update/<int:pk>', CustomerUpdateView.as_view(), name='Customer-user-update'),
    path('change_customer_status/<int:pk>/<str:is_active>/',change_customer_status, name='change_customer_status'),

]