from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.urls import reverse
from django.utils.html import format_html
import pandas as pd
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DeleteView, UpdateView, TemplateView
from django.db.models import Q, Sum, F, IntegerField, Max, Value, CharField, OuterRef
from application.custom_classes import AjayDatatableView, AdminRequiredMixin, UserRequiredMixin
from .forms import CategoryForm,SubCategoriesForm,ProductForm,ProductImportForm,BrandForm,ProductImageForm
from .models import *
from django.http import HttpResponse
from django.views import View
import pandas as pd
import openpyxl
import xlsxwriter


# Category view #
class CategoryCreateView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/form.html'
    success_message = "Category created successfully"
    success_url = reverse_lazy('category-list')

class ListCategoryView(AdminRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'category/list.html'

class ListCategoryJson(AdminRequiredMixin, AjayDatatableView):
    model = Category
    columns = ['CategoryName', 'CategoryDescription','actions']
    exclude_from_search_columns = ['actions']

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
                reverse('category-update', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-xs" data-url={} role="button">Delete</a>'.format(
                reverse('category-delete', kwargs={'pk': row.pk}))
            return edit_action + delete_action
        else:
            return super(ListCategoryJson, self).render_column(row, column)

class CategoryUpdateView(AdminRequiredMixin, LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Category
    template_name = 'category/form.html'
    form_class = CategoryForm
    success_message = "Category updated successfully"
    success_url = reverse_lazy('category-list')


class DeleteCategoryView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Category
    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)


# Subcategory view #

class SubCategoryCreateView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin,CreateView):
    model = SubCategories
    form_class = SubCategoriesForm
    template_name = 'subcategory/form.html'
    success_message = "Category created successfully"
    success_url = reverse_lazy('subcategory-list')
    
    

class ListSubCategoryView(AdminRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'subcategory/list.html'
    
    

class ListSubCategoryJson(AdminRequiredMixin, AjayDatatableView):
    model = SubCategories
    columns = ['name', 'description','parent_category','actions']
    exclude_from_search_columns = ['actions']

    def filter_queryset(self, qs):
        search_value = self.request.GET.get('search[value]', None)
        if search_value:
            qs = qs.filter(
                Q(name__icontains=search_value) | Q(parent_category__CategoryName__icontains=search_value)
            )
        return qs

    def render_column(self, row, column):
        if column == 'is_active':
            if row.is_active:
                return '<span class="badge badge-success">Active</span>'
            else:
                return '<span class="badge badge-danger">Inactive</span>'

        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-xs mr-1 text-white">Edit</a>'.format(
                reverse('subcategory-update', kwargs={'pk': row.pk}))
            return edit_action
        else:
            return super(ListSubCategoryJson, self).render_column(row, column)
        

class SubCategoryUpdateView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SubCategories
    template_name = 'subcategory/form.html'
    form_class = SubCategoriesForm
    success_message = "SubCategory updated successfully"
    success_url = reverse_lazy('subcategory-list')


class BrandListView(AdminRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'brand/list.html'


class BrandListJson(AdminRequiredMixin, AjayDatatableView):
    model = Brand
    columns = ['name','description','actions']
    exclude_from_search_columns = ['actions']

    def get_initial_queryset(self):
        return self.model.objects.all()

    def render_column(self, row, column):
        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-xs mr-1 text-white">Edit</a>'.format(
                reverse('brand-edit', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-xs" data-url={} role="button">Delete</a>'.format(
                reverse('brand-delete', kwargs={'pk': row.pk}))
            return edit_action + delete_action
        else:
            return super(BrandListJson, self).render_column(row, column)


class CreateBrandView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Brand
    form_class = BrandForm
    template_name = "brand/form.html"
    success_message = "Brand created successfully"
    success_url = reverse_lazy('brand-list')


class BrandUpdateView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = 'brand/form.html'
    success_message = "brand Updated successfully"
    success_url = reverse_lazy('brand-list')


class DeleteBrandView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Brand

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)


# Product View #
class ProductCreateView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin,CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/form.html'
    success_message = "Product created successfully"
    success_url = reverse_lazy('product-list')


class ListProductView(AdminRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'product/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = Product.objects.values("merchant_id","merchant__user__email").distinct()
        return context

class ListProductJson(AdminRequiredMixin, AjayDatatableView):
    model = Product
    columns = ['merchant.user.email', 'subcategories_id', 'product_name', 'brand',
               'image', 'product_max_price', 'product_discount_price',
               'product_description', 'product_long_description',
               'in_stock_total', 'actions']
    exclude_from_search_columns = ['actions','subcategories_id','brand']


    def get_initial_queryset(self):
        merchant_id = self.request.GET.get("merchant_id")
        print("check", merchant_id)
        queryset = self.model.objects.all()
        if merchant_id and merchant_id != "Please select merchant":
            queryset = queryset.filter(merchant_id=int(merchant_id))
        return queryset

    def render_column(self, row, column):
        if column == 'is_active':
            return format_html('<span class="badge badge-{0}">{1}</span>', 'success' if row.is_active else 'danger', 'Active' if row.is_active else 'Inactive')
        if column == 'actions':
            edit_url = reverse('product-update', kwargs={'pk': row.pk})
            delete_url = reverse('product-delete', kwargs={'pk': row.pk})
            return format_html('<a href="{0}" role="button" class="btn btn-warning btn-xs mr-1 text-white">Edit</a>'
                               '<a href="javascript:;" class="remove_record btn btn-danger btn-xs" data-url="{1}" role="button">Delete</a>',
                               edit_url, delete_url)
        if column == 'image':
            if row.image:
                image_url = row.image.url
                return format_html('<img src="{0}" alt="Subcategory Image" width="80" height="80">', image_url)
            else:
                return ''
        return super().render_column(row, column)


class ProductUpdateView(AdminRequiredMixin, LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/form.html'
    success_message = "Product Updated successfully"
    success_url = reverse_lazy('product-list')


class DeleteProductView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Product

    def delete(self, request, *args,  **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)
    
    
    
####brand####

        
    

    

########## import view  is underprocess view it's may not work or not work at all!
class ProductImportView(CreateView):
    form_class = ProductImportForm
    template_name = 'product/import.html'
    success_url = reverse_lazy('product-list')

    def form_valid(self, form):
        excel_file = self.request.FILES.get('excel_file')
        if excel_file:
            try:
                df = pd.read_excel(excel_file)
                for index, row in df.iterrows():
                    product = Product(
                        merchant=row['merchant'],
                        product_name=row['product_name'],
                        brand=row['brand'],
                        image=row['image'],
                        product_max_price=row['product_max_price'],
                        product_discount_price=row['product_discount_price'],
                        product_description=row['product_description'],
                        product_long_description=row['product_long_description'],
                        in_stock_total=row['in_stock_total']
                        # we will add more filed here..........
                    )
                    product.save()

                messages.success(self.request, 'Products imported successfully.')
                return HttpResponseRedirect(self.get_success_url())
            
            except Exception as e:
                messages.error(self.request, 'Error importing products')
        else:
            messages.error(self.request, 'somthing wrong with file please try again ')

        return super().form_invalid(form)





class ProductExportView(View):
    def get(self, request, *args, **kwargs):
        merchant = request.GET.get('merchant')
        products = Product.objects.all()
        if merchant != "--Select Merchant--" and merchant:
            products = products.filter(merchant__user__email=merchant)
        else:
            products = Product.objects.all()

        output = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        output['Content-Disposition'] = 'attachment; filename=product_export.xlsx'
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        header = ['Product Name', 'Merchant', 'Subcategory', 'Brand', 'Product Max Price', 'Product Discount Price', 'Product Description', 'Product Long Description', 'In Stock Total']
        for col_num, header_label in enumerate(header):
            worksheet.write(0, col_num, header_label)
        for row_num, product in enumerate(products, start=1):
            row_data = [product.product_name, product.merchant.user.first_name, product.subcategories_id.name, product.brand, product.product_max_price, product.product_discount_price, product.product_description, product.product_long_description, product.in_stock_total]
            for col_num, value in enumerate(row_data):
                worksheet.write(row_num, col_num, value)
        workbook.close()
        return output


class ProductImgae(AdminRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'productimage/list.html'


class ProductImageCreateView(View):
    template_name = 'productimage/form.html'

    def get(self, request, *args, **kwargs):
        form = ProductImageForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image-list')
        return render(request, self.template_name, {'form': form})


class ImgaeListJson(AdminRequiredMixin, AjayDatatableView):
    model = ProductImage
    columns = ['product','image1','image2','image3','image4','description','actions']
    exclude_from_search_columns = ['actions']

    def get_initial_queryset(self):
        return self.model.objects.all()

    def render_column(self, row, column):
        if column == 'actions':
            edit_action = '<a href={} role="button" class="btn btn-warning btn-xs mr-1 text-white">Edit</a>'.format(
                reverse('product_image_update', kwargs={'pk': row.pk}))
            delete_action = '<a href="javascript:;" class="remove_record btn btn-danger btn-xs" data-url={} role="button">Delete</a>'.format(
                reverse('image-delete', kwargs={'pk': row.pk}))
            return edit_action + delete_action

        if column == 'image1':
            if row.image1:
                image_url = row.image1.url
                return format_html('<img src="{0}" alt="Subcategory Image" width="80" height="80">', image_url)
            else:
                return ''
        if column == 'image2':
            if row.image2:
                image_url = row.image2.url
                return format_html('<img src="{0}" alt="Subcategory Image" width="80" height="80">', image_url)
            else:
                return ''
        if column == 'image3':
            if row.image3:
                image_url = row.image3.url
                return format_html('<img src="{0}" alt="Subcategory Image" width="80" height="80">', image_url)
            else:
                return ''
        if column == 'image4':
            if row.image4:
                image_url = row.image4.url
                return format_html('<img src="{0}" alt="Subcategory Image" width="80" height="80">', image_url)
            else:
                return ''

        else:
            return super(ImgaeListJson, self).render_column(row, column)



class ProductImageUpdateView(View):
    template_name = 'productimage/form.html'

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(ProductImage, pk=kwargs['pk'])
        form = ProductImageForm(instance=instance)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        instance = get_object_or_404(ProductImage, pk=kwargs['pk'])
        form = ProductImageForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('image-list')
        return render(request, self.template_name, {'form': form})


class DeleteProductImageView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    model = ProductImage

    def delete(self, request, *args,  **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return JsonResponse(payload)