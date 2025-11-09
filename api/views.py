from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission, IsAdminUser
from base.models import Product, ProductGallery, User
from .serializers import ProductSerializer, ProductGallerySerializer, UserSerializer
from django.shortcuts import HttpResponse
from rest_framework import status
from django.shortcuts import get_object_or_404

# Custom Permissions
class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'employee'

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'manager'

# Handle Users IDs
def get_user_by_role(user_id, role):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None, Response({"error": "User with this ID does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    if user.role != role:
        return None, Response({"error": f"User with this ID is not a {role}."}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = UserSerializer(user)
    return user, Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getRoutes(request):
  routes = [
    'GET  /api',
    'GET  /api/products',
    'GET  /api/products/:id',
    'GET  /api/employees',
    'GET  /api/employees/:id',
    'GET  /api/managers',
    'GET  /api/managers/:id',
  ]
  return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def getProducts(request):
  products = Product.objects.all()
  serializer = ProductSerializer(products, many = True)
  return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def getProduct(request, id):
  product = Product.objects.get(id=id)
  serializer = ProductSerializer(product, many = False)
  return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsManager, IsEmployee])
def getCustomers(request):
  customers = User.objects.filter(role='customer')
  serializer = UserSerializer(customers, many = True)
  return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsManager])
def getEmployees(request):
  employees = User.objects.filter(role='employee')
  serializer = UserSerializer(employees, many = True)
  return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getManagers(request):
  managers = User.objects.filter(role='manager')
  serializer = UserSerializer(managers, many = True)
  return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsManager])
def getEmployee(request, id):
    _, response = get_user_by_role(id, 'employee')
    return response

@api_view(['GET'])
@permission_classes([IsManager, IsEmployee])
def getCustomer(request, id):
    _, response = get_user_by_role(id, 'customer')
    return response

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getManager(request, id):
    _, response = get_user_by_role(id, 'manager')
    return response
