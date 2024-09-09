
from django.urls import path
from sales.views import invoice_views as views


urlpatterns = [
	path('api/v1/invoice/all/',views.getAllInvoice),

	path('api/v1/invoice/without_pagination/all/', views.getAllInvoiceWithoutPagination),

	path('api/v1/invoice/<int:pk>', views.getAInvoice),

	path('api/v1/invoice/search/', views.searchInvoice),

	path('api/v1/invoice/create/', views.createInvoice),

	path('api/v1/invoice/update/<int:pk>', views.updateInvoice),

	path('api/v1/invoice/delete/<int:pk>', views.deleteInvoice),

]