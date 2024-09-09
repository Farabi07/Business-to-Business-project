
from django.urls import path
from core.views import product_review_views as views


urlpatterns = [
	path('api/v1/product_review/all/',views.getAllProductReview),

	path('api/v1/product_review/without_pagination/all/', views.getAllProductReviewWithoutPagination),

	path('api/v1/product_review/<int:pk>', views.getAProductReview),

	path('api/v1/product_review/search/', views.searchProductReview),

	path('api/v1/product_review/create/', views.createProductReview),

	path('api/v1/product_review/update/<int:pk>', views.updateProductReview),

	path('api/v1/product_review/delete/<int:pk>', views.deleteProductReview),

]