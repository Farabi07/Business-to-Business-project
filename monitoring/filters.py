from monitoring.models import *
from django_filters import rest_framework as filters





class AuditFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Audit
        fields = ['name', ]


class NotificationFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Notification
        fields = ['name', ]
