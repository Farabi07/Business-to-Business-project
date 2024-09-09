from django.contrib import admin

from monitoring.models import *



# Register your models here.

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Notification._meta.fields]
	
@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Audit._meta.fields]