from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import has_permissions
from sales.models import BidHistory
from sales.serializers import BidHistorySerializer, BidHistoryListSerializer
from sales.filters import BidHistoryFilter

from commons.enums import PermissionEnum
from commons.pagination import Pagination




# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		
		OpenApiParameter("size"),
  ],
	request=BidHistorySerializer,
	responses=BidHistorySerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllBidHistory(request):
	bid = BidHistory.objects.all()
	total_elements = bid.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	bid = pagination.paginate_data(bid)

	serializer = BidHistoryListSerializer(bid, many=True)

	response = {
		'bid': serializer.data,
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
	request=BidHistorySerializer,
	responses=BidHistorySerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllBidHistoryWithoutPagination(request):
	bid = BidHistory.objects.all()

	serializer = BidHistoryListSerializer(bid, many=True)

	return Response({'bid': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=BidHistorySerializer, responses=BidHistorySerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getABidHistory(request, pk):
	try:
		bid = BidHistory.objects.get(pk=pk)
		serializer = BidHistorySerializer(bid)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"BidHistory id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=BidHistorySerializer, responses=BidHistorySerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchBidHistory(request):
	bid = BidHistoryFilter(request.GET, queryset=BidHistory.objects.all())
	bid = bid.qs

	print('searched_products: ', bid)

	total_elements = bid.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	bid = pagination.paginate_data(bid)

	serializer = BidHistoryListSerializer(bid, many=True)

	response = {
		'bid': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(bid) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no bid matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=BidHistorySerializer, responses=BidHistorySerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createBidHistory(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value

	serializer = BidHistorySerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=BidHistorySerializer, responses=BidHistorySerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updateBidHistory(request,pk):
	try:
		bid = BidHistory.objects.get(pk=pk)
		data = request.data
		serializer = BidHistorySerializer(bid, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"BidHistory id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=BidHistorySerializer, responses=BidHistorySerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deleteBidHistory(request, pk):
	try:
		bid = BidHistory.objects.get(pk=pk)
		bid.delete()
		return Response({'detail': f'BidHistory id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"BidHistory id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

