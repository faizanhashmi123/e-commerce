from django.urls import path
from .views import *

urlpatterns = [
    # category url #
    path('category/list/', ListCategoryView.as_view(), name='category-list'),
    path('create/', CategoryCreateView.as_view(), name='create_category'),
    path('category_create/ajx/list/', ListCategoryJson.as_view(), name='category-ajax-list'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('category/delete/<int:pk>', DeleteCategoryView.as_view(), name='category-delete'),
    # subcategory url #
    path('subcategory/list/', ListSubCategoryView.as_view(), name='subcategory-list'),
    path('create-subcategory/', SubCategoryCreateView.as_view(), name='create_subcategory'),
    path('subcategory_create/ajx/list/', ListSubCategoryJson.as_view(), name='subcategory-ajax-list'),
    path('subcategory/<int:pk>/update/', SubCategoryUpdateView.as_view(), name='subcategory-update'),
    # product urls #
    path('create-product/', ProductCreateView.as_view(), name='create_product'),
    path('product/list/', ListProductView.as_view(), name='product-list'),
    path('product_create/ajx/list/', ListProductJson.as_view(), name='product-ajax-list'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/delete/<int:pk>', DeleteProductView.as_view(), name='product-delete'),

    # brand urls #
    path('brand/list/', BrandListView.as_view(), name='brand-list'),
    path('brand/list/ajax/', BrandListJson.as_view(), name='brand-list-ajax'),
    path('brand/create/', CreateBrandView.as_view(), name='create-brand'),
    path('brand/<int:pk>/update/', BrandUpdateView.as_view(), name='brand-edit'),
    path('brand/delete/<int:pk>', DeleteBrandView.as_view(), name='brand-delete'),

    #product image #
    path('image/list/', ProductImgae.as_view(), name='image-list'),
    path('image/create/', ProductImageCreateView.as_view(), name='create-image'),
    path('image/list/ajax/', ImgaeListJson.as_view(), name='image-list-ajax'),
    path('product_image/update/<int:pk>/', ProductImageUpdateView.as_view(), name='product_image_update'),
    path('image/delete/<int:pk>', DeleteProductImageView.as_view(), name='image-delete'),
    
    


    #import and export
    path('import/create/product/', ProductImportView.as_view(), name='create_import_product'),
    path('export-excel/', ProductExportView.as_view(), name='create_export_product'),


    
]