from django.contrib import admin

from core.models import *



# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Company._meta.fields]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Contact._meta.fields]
	
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Product._meta.fields]

@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
	list_display = [field.name for field in ProductType._meta.fields]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Category._meta.fields]

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
	list_display = [field.name for field in ProductReview._meta.fields]