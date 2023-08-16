from django import forms
from .models import Category,SubCategories,Product,ProductImport, Brand,ProductImage


class ProductImportForm(forms.ModelForm):
    class Meta:
        model = ProductImport
        fields = ['file_name']
        
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields =['CategoryName','CategoryDescription']
        
        
class SubCategoriesForm(forms.ModelForm):
    class Meta:
        model = SubCategories
        fields = ['name', 'description', 'parent_category']
        
        
        
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description']        
        

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['merchant', 'subcategories_id', 'product_name',
                  'brand', 'image',
                  'product_max_price', 'product_discount_price',
                  'product_description',
                  'product_long_description', 'in_stock_total']


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = '__all__'

