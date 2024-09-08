from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'companies'
        ordering = ('-id', )

    def __str__(self):
        return self.name


class Contact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='contacts')
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company.name}"

class ProductType(models.Model):
    name = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.name
    
class ProductCategory(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    product_category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='products_category', null=True, blank=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name='products_type', null=True, blank=True)
    product_image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name