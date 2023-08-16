from django.urls import path
from .views import CreateMerchantView, ListMerchantView, ListMerchantViewJson, Change_Merchant_Status, DeleteMerchantView, UpdateMerchantView

urlpatterns = [
    path('register/merchant/', CreateMerchantView.as_view(), name='register-merchant'),
    path('merchent/list/', ListMerchantView.as_view(), name='merchant-list'),
    path('merchent/list/ajax', ListMerchantViewJson.as_view(), name='merchant-list-ajax'),
    
    path('change_merchant_status/<int:pk>/<str:is_active>/', Change_Merchant_Status,
         name='change-merchant-status'),
    
    path('delete/<int:pk>', DeleteMerchantView.as_view(), name='merchant-delete'),
    path('update/<int:pk>', UpdateMerchantView.as_view(), name='merchant-update'),
    
    
    
]