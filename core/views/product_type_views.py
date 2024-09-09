from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import has_permissions
from core.models import ProductType
from core.serializers import ProductTypeSerializer, ProductTypeListSerializer
from core.filters import ProductTypeFilter

from commons.enums import PermissionEnum
from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		
		OpenApiParameter("size"),
  ],
	request=ProductTypeSerializer,
	responses=ProductTypeSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllProductType(request):
	product_types = ProductType.objects.all()
	total_elements = product_types.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	product_types = pagination.paginate_data(product_types)

	serializer = ProductTypeListSerializer(product_types, many=True)

	response = {
		'product_types': serializer.data,
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
	request=ProductTypeSerializer,
	responses=ProductTypeSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllProductTypeWithoutPagination(request):
	product_types = ProductType.objects.all()

	serializer = ProductTypeListSerializer(product_types, many=True)

	return Response({'product_types': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=ProductTypeSerializer, responses=ProductTypeSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getAProductType(request, pk):
	try:
		product_types = ProductType.objects.get(pk=pk)
		serializer = ProductTypeSerializer(product_types)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductType id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductTypeSerializer, responses=ProductTypeSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchProductType(request):
	product_types = ProductTypeFilter(request.GET, queryset=ProductType.objects.all())
	product_types = product_types.qs

	print('searched_products: ', product_types)

	total_elements = product_types.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	product_types = pagination.paginate_data(product_types)

	serializer = ProductTypeListSerializer(product_types, many=True)

	response = {
		'product_types': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(product_types) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no product_types matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductTypeSerializer, responses=ProductTypeSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createProductType(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value

	serializer = ProductTypeSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductTypeSerializer, responses=ProductTypeSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updateProductType(request,pk):
	try:
		product_types = ProductType.objects.get(pk=pk)
		data = request.data
		serializer = ProductTypeSerializer(product_types, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductType id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductTypeSerializer, responses=ProductTypeSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deleteProductType(request, pk):
	try:
		product_types = ProductType.objects.get(pk=pk)
		product_types.delete()
		return Response({'detail': f'ProductType id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductType id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

