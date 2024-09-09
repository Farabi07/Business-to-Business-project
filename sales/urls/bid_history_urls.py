
from django.urls import path
from sales.views import bid_history_views as views


urlpatterns = [
	path('api/v1/bid_history/all/',views.getAllBidHistory),

	path('api/v1/bid_history/without_pagination/all/', views.getAllBidHistoryWithoutPagination),

	path('api/v1/bid_history/<int:pk>', views.getABidHistory),

	path('api/v1/bid_history/search/', views.searchBidHistory),

	path('api/v1/bid_history/create/', views.createBidHistory),

	path('api/v1/bid_history/update/<int:pk>', views.updateBidHistory),

	path('api/v1/bid_history/delete/<int:pk>', views.deleteBidHistory),

]