from django.core.exceptions import ObjectDoesNotExist, ValidationError

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import OpenApiParameter, extend_schema

from authentication.decorators import has_permissions
from sales.models import Invoice
from sales.serializers import InvoiceSerializer, InvoiceListSerializer
from sales.filters import InvoiceFilter

from commons.enums import PermissionEnum
from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		OpenApiParameter("size"),
  ],
	request=InvoiceSerializer,
	responses=InvoiceSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllInvoice(request):
	invoice = Invoice.objects.all()
	total_elements = invoice.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	invoice = pagination.paginate_data(invoice)

	serializer = InvoiceListSerializer(invoice, many=True)

	response = {
		'invoice': serializer.data,
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
	request=InvoiceSerializer,
	responses=InvoiceSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllInvoiceWithoutPagination(request):
	invoice = Invoice.objects.all()

	serializer = InvoiceListSerializer(invoice, many=True)

	return Response({'invoice': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=InvoiceSerializer, responses=InvoiceSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getAInvoice(request, pk):
	try:
		invoice = Invoice.objects.get(pk=pk)
		serializer = InvoiceSerializer(invoice)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Invoice id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=InvoiceSerializer, responses=InvoiceSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchInvoice(request):
	invoice = InvoiceFilter(request.GET, queryset=Invoice.objects.all())
	invoice = invoice.qs

	print('searched_products: ', invoice)

	total_elements = invoice.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	invoice = pagination.paginate_data(invoice)

	serializer = InvoiceListSerializer(invoice, many=True)

	response = {
		'invoice': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(invoice) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no invoice matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=InvoiceSerializer, responses=InvoiceSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createInvoice(request):
	data = request.data
	filtered_data = {}
	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value
			
	serializer = InvoiceSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=InvoiceSerializer, responses=InvoiceSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updateInvoice(request,pk):
	try:
		invoice = Invoice.objects.get(pk=pk)
		data = request.data
		serializer = InvoiceSerializer(invoice, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"Invoice id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=InvoiceSerializer, responses=InvoiceSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deleteInvoice(request, pk):
	try:
		invoice = Invoice.objects.get(pk=pk)
		invoice.delete()
		return Response({'detail': f'Invoice id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Invoice id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
