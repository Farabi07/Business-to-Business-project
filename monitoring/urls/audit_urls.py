
from django.urls import path
from monitoring.views import audit_views as views


urlpatterns = [
	path('api/v1/audit/all/', views.getAllAudit),

	path('api/v1/audit/without_pagination/all/', views.getAllAuditWithoutPagination),

	path('api/v1/audit/<int:pk>', views.getAAudit),

	path('api/v1/audit/search/', views.searchAudit),

	path('api/v1/audit/create/', views.createAudit),

	path('api/v1/audit/update/<int:pk>', views.updateAudit),

	path('api/v1/audit/delete/<int:pk>', views.deleteAudit),



]