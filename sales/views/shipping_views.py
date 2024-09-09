from django.core.exceptions import ObjectDoesNotExist, ValidationError

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import OpenApiParameter, extend_schema

from authentication.decorators import has_permissions
from sales.models import ShippingDetails
from sales.serializers import ShippingDetailsSerializer, ShippingDetailsListSerializer
from sales.filters import ShippingDetailsFilter

from commons.enums import PermissionEnum
from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=ShippingDetailsSerializer,
	responses=ShippingDetailsSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllShippingDetails(request):
	shipping = ShippingDetails.objects.all()
	total_elements = shipping.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	shipping = pagination.paginate_data(shipping)

	serializer = ShippingDetailsListSerializer(shipping, many=True)

	response = {
		'shipping': serializer.data,
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
	request=ShippingDetailsSerializer,
	responses=ShippingDetailsSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllShippingDetailsWithoutPagination(request):
	shipping = ShippingDetails.objects.all()

	serializer = ShippingDetailsListSerializer(shipping, many=True)

	return Response({'shipping': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=ShippingDetailsSerializer, responses=ShippingDetailsSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getAShippingDetails(request, pk):
	try:
		shipping = ShippingDetails.objects.get(pk=pk)
		serializer = ShippingDetailsSerializer(shipping)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"ShippingDetails id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ShippingDetailsSerializer, responses=ShippingDetailsSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchShippingDetails(request):
	shipping = ShippingDetailsFilter(request.GET, queryset=ShippingDetails.objects.all())
	shipping = shipping.qs

	print('searched_products: ', shipping)

	total_elements = shipping.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	shipping = pagination.paginate_data(shipping)

	serializer = ShippingDetailsListSerializer(shipping, many=True)

	response = {
		'shipping': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(shipping) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no shipping matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ShippingDetailsSerializer, responses=ShippingDetailsSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createShippingDetails(request):
	data = request.data
	filtered_data = {}
	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value
			
	serializer = ShippingDetailsSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ShippingDetailsSerializer, responses=ShippingDetailsSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updateShippingDetails(request,pk):
	try:
		shipping = ShippingDetails.objects.get(pk=pk)
		data = request.data
		serializer = ShippingDetailsSerializer(shipping, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"ShippingDetails id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ShippingDetailsSerializer, responses=ShippingDetailsSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deleteShippingDetails(request, pk):
	try:
		shipping = ShippingDetails.objects.get(pk=pk)
		shipping.delete()
		return Response({'detail': f'ShippingDetails id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"ShippingDetails id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
