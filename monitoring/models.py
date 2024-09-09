from django.db import models
from core.models import *
from django.conf import settings


# Create your models here.
class Notification(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=50,
        choices=[
            ('Bid Update', 'Bid Update'),
            ('Order Update', 'Order Update'),
            ('Payment Reminder', 'Payment Reminder'),
            ('General', 'General')
        ],
        default='General'
    )
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)


    class Meta:
        verbose_name_plural = 'Notification'
        ordering = ('-id', )

    def __str__(self):
        return f"Notification {self.id} - {self.notification_type}"


class Audit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50)  # e.g., Created, Updated, Deleted
    model_name = models.CharField(max_length=50)  # The model that was changed
    object_id = models.PositiveIntegerField()  # The primary key of the object changed
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField()  # Store details about what was changed

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.SET_NULL, related_name="+", null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Audit'
        ordering = ('-id', )
    def __str__(self):
        return f"{self.action} - {self.model_name} ID {self.object_id} by {self.user.username if self.user else 'System'}"
