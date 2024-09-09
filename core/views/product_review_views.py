from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import  extend_schema, OpenApiParameter

from authentication.decorators import has_permissions
from core.models import ProductReview
from core.serializers import ProductReviewSerializer, ProductReviewListSerializer
from core.filters import ProductReviewFilter

from commons.enums import PermissionEnum
from commons.pagination import Pagination


# Create your views here.

@extend_schema(
	parameters=[
		OpenApiParameter("page"),
		
		OpenApiParameter("size"),
  ],
	request=ProductReviewSerializer,
	responses=ProductReviewSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllProductReview(request):
	review = ProductReview.objects.all()
	total_elements = review.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	review = pagination.paginate_data(review)

	serializer = ProductReviewListSerializer(review, many=True)

	response = {
		'review': serializer.data,
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
	request=ProductReviewSerializer,
	responses=ProductReviewSerializer
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_LIST_VIEW.name])
def getAllProductReviewWithoutPagination(request):
	review = ProductReview.objects.all()

	serializer = ProductReviewListSerializer(review, many=True)

	return Response({'review': serializer.data}, status=status.HTTP_200_OK)




@extend_schema(request=ProductReviewSerializer, responses=ProductReviewSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def getAProductReview(request, pk):
	try:
		review = ProductReview.objects.get(pk=pk)
		serializer = ProductReviewSerializer(review)
		return Response(serializer.data, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductReview id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductReviewSerializer, responses=ProductReviewSerializer)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DETAILS_VIEW.name])
def searchProductReview(request):
	review = ProductReviewFilter(request.GET, queryset=ProductReview.objects.all())
	review = review.qs

	print('searched_products: ', review)

	total_elements = review.count()

	page = request.query_params.get('page')
	size = request.query_params.get('size')

	# Pagination
	pagination = Pagination()
	pagination.page = page
	pagination.size = size
	review = pagination.paginate_data(review)

	serializer = ProductReviewListSerializer(review, many=True)

	response = {
		'review': serializer.data,
		'page': pagination.page,
		'size': pagination.size,
		'total_pages': pagination.total_pages,
		'total_elements': total_elements,
	}

	if len(review) > 0:
		return Response(response, status=status.HTTP_200_OK)
	else:
		return Response({'detail': f"There are no review matching your search"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductReviewSerializer, responses=ProductReviewSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_CREATE.name])
def createProductReview(request):
	data = request.data
	filtered_data = {}

	for key, value in data.items():
		if value != '' and value != '0':
			filtered_data[key] = value

	serializer = ProductReviewSerializer(data=filtered_data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	else:
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductReviewSerializer, responses=ProductReviewSerializer)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_UPDATE.name, PermissionEnum.PERMISSION_PARTIAL_UPDATE.name])
def updateProductReview(request,pk):
	try:
		review = ProductReview.objects.get(pk=pk)
		data = request.data
		serializer = ProductReviewSerializer(review, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductReview id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)




@extend_schema(request=ProductReviewSerializer, responses=ProductReviewSerializer)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @has_permissions([PermissionEnum.PERMISSION_DELETE.name])
def deleteProductReview(request, pk):
	try:
		review = ProductReview.objects.get(pk=pk)
		review.delete()
		return Response({'detail': f'ProductReview id - {pk} is deleted successfully'}, status=status.HTTP_200_OK)
	except ObjectDoesNotExist:
		return Response({'detail': f"ProductReview id - {pk} doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)

