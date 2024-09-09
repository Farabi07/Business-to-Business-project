
from django.urls import path
from sales.views import order_item_views as views


urlpatterns = [
	path('api/v1/order_item/all/',views.getAllOrderItem),

	path('api/v1/order_item/without_pagination/all/', views.getAllOrderItemWithoutPagination),

	path('api/v1/order_item/<int:pk>', views.getAOrderItem),

	path('api/v1/order_item/search/', views.searchOrderItem),

	path('api/v1/order_item/create/', views.createOrderItem),

	path('api/v1/order_item/update/<int:pk>', views.updateOrderItem),

	path('api/v1/order_item/delete/<int:pk>', views.deleteOrderItem),

]