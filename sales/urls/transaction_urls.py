
from django.urls import path
from sales.views import transaction_views as views


urlpatterns = [
	path('api/v1/transaction/all/',views.getAllTransaction),

	path('api/v1/transaction/without_pagination/all/', views.getAllTransactionWithoutPagination),

	path('api/v1/transaction/<int:pk>', views.getATransaction),

	path('api/v1/transaction/search/', views.searchTransaction),

	path('api/v1/transaction/create/', views.createTransaction),

	path('api/v1/transaction/update/<int:pk>', views.updateTransaction),

	path('api/v1/transaction/delete/<int:pk>', views.deleteTransaction),

]