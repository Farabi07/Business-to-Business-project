from django.core.exceptions import ObjectDoesNotExist, ValidationError

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import OpenApiParameter, extend_schema

from authentication.decorators import has_permissions
from sales.models import Transaction
from sales.serializers import TransactionSerializer, TransactionListSerializer
from sales.filters import TransactionFilter

from commons.enums import PermissionEnum
from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=TransactionSerializer,
	responses=TransactionSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllTransaction(request):
	transaction = Transaction.objects.all()
	total_elements = transaction.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	transaction = pagination.paginate_data(transaction)

	serializer = TransactionListSerializer(transaction, many=True)

	response = {
		'transaction': serializer.data,
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
	request=TransactionSerializer,
	responses=TransactionSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllTransactionWithoutPagination(request):
	transaction = Transaction.objects.all()

	serializer = TransactionListSerializer(transaction, many=True)

	return Response({'transaction': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=TransactionSerializer, responses=TransactionSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getATransaction(request, pk):
	try:
		transaction = Transaction.objects.get(pk=pk)
		serializer = TransactionSerializer(transaction)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Transaction id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=TransactionSerializer, responses=TransactionSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchTransaction(request):
	transaction = TransactionFilter(request.GET, queryset=Transaction.objects.all())
	transaction = transaction.qs

	print('searched_products: ', transaction)

	total_elements = transaction.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	transaction = pagination.paginate_data(transaction)

	serializer = TransactionListSerializer(transaction, many=True)

	response = {
		'transaction': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(transaction) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no transaction matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=TransactionSerializer, responses=TransactionSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createTransaction(request):
	data = request.data
	filtered_data = {}
	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value
			
	serializer = TransactionSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=TransactionSerializer, responses=TransactionSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updateTransaction(request,pk):
	try:
		transaction = Transaction.objects.get(pk=pk)
		data = request.data
		serializer = TransactionSerializer(transaction, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"Transaction id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=TransactionSerializer, responses=TransactionSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deleteTransaction(request, pk):
	try:
		transaction = Transaction.objects.get(pk=pk)
		transaction.delete()
		return Response({'detail': f'Transaction id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Transaction id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
