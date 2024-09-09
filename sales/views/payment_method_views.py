from django.core.exceptions import ObjectDoesNotExist, ValidationError

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import OpenApiParameter, extend_schema

from authentication.decorators import has_permissions
from sales.models import PaymentMethod
from sales.serializers import PaymentMethodSerializer, PaymentMethodListSerializer
from sales.filters import PaymentMethodFilter

from commons.enums import PermissionEnum
from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=PaymentMethodSerializer,
	responses=PaymentMethodSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllPaymentMethod(request):
	payment_method = PaymentMethod.objects.all()
	total_elements = payment_method.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	payment_method = pagination.paginate_data(payment_method)

	serializer = PaymentMethodListSerializer(payment_method, many=True)

	response = {
		'payment_method': serializer.data,
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
	request=PaymentMethodSerializer,
	responses=PaymentMethodSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllPaymentMethodWithoutPagination(request):
	payment_method = PaymentMethod.objects.all()

	serializer = PaymentMethodListSerializer(payment_method, many=True)

	return Response({'payment_method': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=PaymentMethodSerializer, responses=PaymentMethodSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getAPaymentMethod(request, pk):
	try:
		payment_method = PaymentMethod.objects.get(pk=pk)
		serializer = PaymentMethodSerializer(payment_method)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"PaymentMethod id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=PaymentMethodSerializer, responses=PaymentMethodSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchPaymentMethod(request):
	payment_method = PaymentMethodFilter(request.GET, queryset=PaymentMethod.objects.all())
	payment_method = payment_method.qs

	print('searched_products: ', payment_method)

	total_elements = payment_method.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	payment_method = pagination.paginate_data(payment_method)

	serializer = PaymentMethodListSerializer(payment_method, many=True)

	response = {
		'payment_method': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(payment_method) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no payment_method matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=PaymentMethodSerializer, responses=PaymentMethodSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createPaymentMethod(request):
	data = request.data
	filtered_data = {}
	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value
			
	serializer = PaymentMethodSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=PaymentMethodSerializer, responses=PaymentMethodSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updatePaymentMethod(request,pk):
	try:
		payment_method = PaymentMethod.objects.get(pk=pk)
		data = request.data
		serializer = PaymentMethodSerializer(payment_method, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"PaymentMethod id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=PaymentMethodSerializer, responses=PaymentMethodSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deletePaymentMethod(request, pk):
	try:
		payment_method = PaymentMethod.objects.get(pk=pk)
		payment_method.delete()
		return Response({'detail': f'PaymentMethod id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"PaymentMethod id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
