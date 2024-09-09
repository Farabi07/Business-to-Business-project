from sales.models import *
from django_filters import rest_framework as filters





class OrderFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Order
        fields = ['name', ]



class OrderItemFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = OrderItem
        fields = ['name', ]

class BidFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Bid
        fields = ['name', ]

class BidHistoryFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = BidHistory
        fields = ['name', ]


class InvoiceFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Invoice
        fields = ['name', ]

class PaymentMethodFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = PaymentMethod
        fields = ['name', ]

class TransactionFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Transaction
        fields = ['name', ]

class ShippingDetailsFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = ShippingDetails
        fields = ['name', ]