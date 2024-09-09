
from django.urls import path
from sales.views import bid_views as views


urlpatterns = [
	path('api/v1/bid/all/',views.getAllBid),

	path('api/v1/bid/without_pagination/all/', views.getAllBidWithoutPagination),

	path('api/v1/bid/<int:pk>', views.getABid),

	path('api/v1/bid/search/', views.searchBid),

	path('api/v1/bid/create/', views.createBid),

	path('api/v1/bid/update/<int:pk>', views.updateBid),

	path('api/v1/bid/delete/<int:pk>', views.deleteBid),

]