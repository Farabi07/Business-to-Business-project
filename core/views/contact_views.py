from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import has_permissions
from core.models import Contact
from core.serializers import ContactSerializer, ContactListSerializer
from core.filters import ContactFilter

from commons.enums import PermissionEnum
from commons.pagination import Pagination


# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		
		OpenApiParameter("size"),
  ],
	request=ContactSerializer,
	responses=ContactSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllContact(request):
	contacts = Contact.objects.all()
	total_elements = contacts.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	contacts = pagination.paginate_data(contacts)

	serializer = ContactListSerializer(contacts, many=True)

	response = {
		'contacts': serializer.data,
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
	request=ContactSerializer,
	responses=ContactSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllContactWithoutPagination(request):
	contacts = Contact.objects.all()

	serializer = ContactListSerializer(contacts, many=True)

	return Response({'contacts': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=ContactSerializer, responses=ContactSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getAContact(request, pk):
	try:
		Contact = Contact.objects.get(pk=pk)
		serializer = ContactSerializer(Contact)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Contact id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ContactSerializer, responses=ContactSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchContact(request):
	contacts = ContactFilter(request.GET, queryset=Contact.objects.all())
	contacts = contacts.qs

	print('searched_products: ', contacts)

	total_elements = contacts.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	contacts = pagination.paginate_data(contacts)

	serializer = ContactListSerializer(contacts, many=True)

	response = {
		'contacts': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(contacts) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no contacts matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ContactSerializer, responses=ContactSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createContact(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value

	serializer = ContactSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ContactSerializer, responses=ContactSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updateContact(request,pk):
	try:
		Contact = Contact.objects.get(pk=pk)
		data = request.data
		serializer = ContactSerializer(Contact, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"Contact id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ContactSerializer, responses=ContactSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deleteContact(request, pk):
	try:
		Contact = Contact.objects.get(pk=pk)
		Contact.delete()
		return Response({'detail': f'Contact id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"Contact id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

