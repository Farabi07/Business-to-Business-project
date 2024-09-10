from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import has_permissions
from monitoring.models import Notification
from monitoring.serializers import NotificationSerializer, NotificationListSerializer
from monitoring.filters import NotificationFilter

from commons.enums import PermissionEnum
from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		
		OpenApiParameter("size"),
  ],
	request=NotificationSerializer,
	responses=NotificationSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllNotification(request):
	notifications = Notification.objects.all()
	total_elements = notifications.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	notifications = pagination.paginate_data(notifications)

	serializer = NotificationListSerializer(notifications, many=True)

	response = {
		'notifications': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	return Response(response, status=status.HTTP_200_OK)




@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=NotificationSerializer,
	responses=NotificationSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllNotificationWithoutPagination(request):
	notifications = Notification.objects.all()

	serializer = NotificationListSerializer(notifications, many=True)

	return Response({'notifications': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=NotificationSerializer, responses=NotificationSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getANotification(request, pk):
	try:
		notification = Notification.objects.get(pk=pk)
		serializer = NotificationSerializer(notification)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Notification id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=NotificationSerializer, responses=NotificationSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchNotification(request):
	notifications = NotificationFilter(request.GET, queryset=Notification.objects.all())
	notifications = notifications.qs

	print('searched_products: ', notifications)

	total_elements = notifications.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	notifications = pagination.paginate_data(notifications)

	serializer = NotificationListSerializer(notifications, many=True)

	response = {
		'notifications': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(notifications) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no notifications matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=NotificationSerializer, responses=NotificationSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createNotification(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value

	serializer = NotificationSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=NotificationSerializer, responses=NotificationSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updateNotification(request,pk):
	try:
		notification = Notification.objects.get(pk=pk)
		data = request.data
		serializer = NotificationSerializer(notification, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"Notification id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=NotificationSerializer, responses=NotificationSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deleteNotification(request, pk):
	try:
		notification = Notification.objects.get(pk=pk)
		notification.delete()
		return Response({'detail': f'Notification id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Notification id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

