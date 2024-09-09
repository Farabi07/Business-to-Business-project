
from django.urls import path
from core.views import company_views as views


urlpatterns = [
	path('api/v1/company/all/',views.getAllCompany),

	path('api/v1/company/without_pagination/all/', views.getAllCompanyWithoutPagination),

	path('api/v1/company/<int:pk>', views.getACompany),

	path('api/v1/company/search/', views.searchCompany),

	path('api/v1/company/create/', views.createCompany),

	path('api/v1/company/update/<int:pk>', views.updateCompany),

	path('api/v1/company/delete/<int:pk>', views.deleteCompany),

]