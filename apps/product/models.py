from django.db import models
from application.custom_models import DateTimeModel
from apps.merchant.models import Merchant
from apps.user.models import User


class ProductImport(models.Model):
    file_name = models.FileField(upload_to='uploads')

class Category(DateTimeModel):
    CategoryName = models.CharField(max_length=100)
    CategoryDescription = models.TextField()

    def __str__(self):
        return self.CategoryName

class SubCategories(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.name
    
    
    
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


    

class Product(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    subcategories_id = models.ForeignKey(SubCategories, on_delete=models.CASCADE, null=True)
    product_name = models.CharField(max_length=255)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    product_max_price = models.CharField(max_length=255,null=True)
    product_discount_price = models.CharField(max_length=255,null=True)
    product_description = models.TextField()
    product_long_description = models.TextField(blank=True, null=True)
    in_stock_total = models.IntegerField(default=1)

    def __str__(self):
        return self.product_name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image1 = models.ImageField(upload_to='product_images/')
    image2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    description = models.TextField(blank=True)

