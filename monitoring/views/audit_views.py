from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import has_permissions
from monitoring.models import Audit
from monitoring.serializers import AuditSerializer, AuditListSerializer
from monitoring.filters import AuditFilter

from commons.enums import PermissionEnum
from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		
		OpenApiParameter("size"),
  ],
	request=AuditSerializer,
	responses=AuditSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllAudit(request):
	aduit = Audit.objects.all()
	total_elements = aduit.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	aduit = pagination.paginate_data(aduit)

	serializer = AuditListSerializer(aduit, many=True)

	response = {
		'aduit': serializer.data,
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
	request=AuditSerializer,
	responses=AuditSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllAuditWithoutPagination(request):
	aduit = Audit.objects.all()

	serializer = AuditListSerializer(aduit, many=True)

	return Response({'aduit': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=AuditSerializer, responses=AuditSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getAAudit(request, pk):
	try:
		aduit = Audit.objects.get(pk=pk)
		serializer = AuditSerializer(aduit)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Audit id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=AuditSerializer, responses=AuditSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchAudit(request):
	aduit = AuditFilter(request.GET, queryset=Audit.objects.all())
	aduit = aduit.qs

	print('searched_products: ', aduit)

	total_elements = aduit.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	aduit = pagination.paginate_data(aduit)

	serializer = AuditListSerializer(aduit, many=True)

	response = {
		'aduit': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(aduit) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no aduit matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=AuditSerializer, responses=AuditSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createAudit(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value

	serializer = AuditSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=AuditSerializer, responses=AuditSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updateAudit(request,pk):
	try:
		aduit = Audit.objects.get(pk=pk)
		data = request.data
		serializer = AuditSerializer(aduit, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"Audit id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=AuditSerializer, responses=AuditSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deleteAudit(request, pk):
	try:
		aduit = Audit.objects.get(pk=pk)
		aduit.delete()
		return Response({'detail': f'Audit id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Audit id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

