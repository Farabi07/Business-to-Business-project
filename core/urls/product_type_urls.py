
from django.urls import path
from core.views import product_type_views as views


urlpatterns = [
	path('api/v1/product_type/all/', views.getAllProductType),

	path('api/v1/product_type/without_pagination/all/', views.getAllProductTypeWithoutPagination),

	path('api/v1/product_type/<int:pk>', views.getAProductType),

	path('api/v1/product_type/search/', views.searchProductType),

	path('api/v1/product_type/create/', views.createProductType),

	path('api/v1/product_type/update/<int:pk>', views.updateProductType),

	path('api/v1/product_type/delete/<int:pk>', views.deleteProductType),



]