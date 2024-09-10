
from django.urls import path
from monitoring.views import notification_views as views


urlpatterns = [
	path('api/v1/notification/all/', views.getAllNotification),

	path('api/v1/notification/without_pagination/all/', views.getAllNotificationWithoutPagination),

	path('api/v1/notification/<int:pk>', views.getANotification),

	path('api/v1/notification/search/', views.searchNotification),

	path('api/v1/notification/create/', views.createNotification),

	path('api/v1/notification/update/<int:pk>', views.updateNotification),

	path('api/v1/notification/delete/<int:pk>', views.deleteNotification),



]