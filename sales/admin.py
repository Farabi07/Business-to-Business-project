from django.contrib import admin

from sales.models import *



# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Order._meta.fields]
	
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = [field.name for field in OrderItem._meta.fields]
	
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Invoice._meta.fields]
	
@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Bid._meta.fields]
	
@admin.register(BidHistory)
class BidHistoryAdmin(admin.ModelAdmin):
	list_display = [field.name for field in BidHistory._meta.fields]
	

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
	list_display = [field.name for field in PaymentMethod._meta.fields]
	
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Transaction._meta.fields]
	
@admin.register(ShippingDetails)
class ShippingDetailsAdmin(admin.ModelAdmin):
	list_display = [field.name for field in ShippingDetails._meta.fields]
	
