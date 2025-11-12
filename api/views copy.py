from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    BasePermission,
    IsAdminUser,
)
from base.models import Product, ProductGallery, User
from .serializers import ProductSerializer, ProductGallerySerializer, UserSerializer
from django.shortcuts import HttpResponse
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


# Custom Permissions
class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        if request.user.id != None:
            return request.user.role == "employee"

class IsManager(BasePermission):
    def has_permission(self, request, view):
        if request.user.id != None:
            return request.user.role == "manager"


# Handle Users IDs
def get_user_by_role(user_id, role):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None, Response(
            {"error": "User with this ID does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if user.role != role:
        return None, Response(
            {"error": f"User with this ID is not a {role}."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = UserSerializer(user)
    return user, Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def getRoutes(request):
    routes = [
        "GET  /api",
        "GET  /api/products",
        "GET  /api/products/:id",
        "GET  /api/employees",
        "GET  /api/employees/:id",
        "GET  /api/managers",
        "GET  /api/managers/:id",
    ]
    return Response(routes)


@api_view(["GET", "POST"])
# @permission_classes([IsAuthenticatedOrReadOnly])
def getProducts(request):
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticatedOrReadOnly])
def getProduct(request, id):
    product = Product.objects.get(id=id)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsManager, IsEmployee])
def getCustomers(request):
    customers = User.objects.filter(role="customer")
    serializer = UserSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
# @login_required(login_url='account_login')
# @permission_classes([IsManager])
def getEmployees(request):
    if request.method == "GET":
        employees = User.objects.filter(role="employee")
        serializer = UserSerializer(employees, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def getManagers(request):
    managers = User.objects.filter(role="manager")
    serializer = UserSerializer(managers, many=True)
    return Response(serializer.data)


#@permission_classes([IsManager])
@api_view(["GET", "PATCH", "PUT", "DELETE"])
def getEmployee(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
      _, response = get_user_by_role(id, "employee")
      return response

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
          user.delete()
          return Response(
              {"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT
          )
    
@api_view(["GET"])
@permission_classes([IsManager, IsEmployee])
def getCustomer(request, id):
    _, response = get_user_by_role(id, "customer")
    return response


@api_view(["GET"])
@permission_classes([IsAdminUser])
def getManager(request, id):
    _, response = get_user_by_role(id, "manager")
    return response
