
from django.urls import path
from sales.views import shipping_views as views


urlpatterns = [
	path('api/v1/shipping_details/all/',views.getAllShippingDetails),

	path('api/v1/shipping_details/without_pagination/all/', views.getAllShippingDetailsWithoutPagination),

	path('api/v1/shipping_details/<int:pk>', views.getAShippingDetails),

	path('api/v1/shipping_details/search/', views.searchShippingDetails),

	path('api/v1/shipping_details/create/', views.createShippingDetails),

	path('api/v1/shipping_details/update/<int:pk>', views.updateShippingDetails),

	path('api/v1/shipping_details/delete/<int:pk>', views.deleteShippingDetails),

]