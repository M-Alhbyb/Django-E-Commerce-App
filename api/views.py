from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
    IsAdminUser,
)
from base.models import Product,  User
from .serializers import ProductSerializer, UserSerializer
from rest_framework import status


class IsEmployeeOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        # Require authentication and employee role for write actions
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, "role", None) == "employee"
        )


class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, "role", None) == "manager"
        )


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

# BASE Views
def UsersView(request, role):
    if request.method == "GET":
        employees = User.objects.filter(role=role)
        serializer = UserSerializer(employees, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def UserView(request, id, role):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        _, response = get_user_by_role(id, role)
        return response

    elif request.method == "PUT":
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        user.delete()
        return Response(
            {"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )


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

@authentication_classes([TokenAuthentication])
@permission_classes([IsEmployeeOrReadOnly])
@api_view(["GET", "POST"])
def ProductsView(request):
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


@authentication_classes([TokenAuthentication])
@permission_classes([IsEmployeeOrReadOnly])
@api_view(["GET", "PUT", "PATCH", "DELETE"])
def ProductView(request, id):
    # check If Product exists
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
        )

    # GET REQUEST
    if request.method == "GET":
        print("GET")
        serializer = ProductSerializer(product, many=False)
        return Response(serializer.data)

    # PUT REQUEST
    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH REQUEST
    elif request.method == "PATCH":
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE REQUEST
    elif request.method == "DELETE":
        product.delete()
        return Response(
            {"message": "Product deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

@authentication_classes([TokenAuthentication])
@permission_classes([IsManagerOrReadOnly])
@api_view(["GET", "POST"])
def EmployeesView(request):
    return UsersView(request, role="employee")


@authentication_classes([TokenAuthentication])
@permission_classes([IsManagerOrReadOnly])
@api_view(["GET", "PUT", "PATCH", "DELETE"])
def EmployeeView(request, id):
    return UserView(request, id, role="employee")


@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
@api_view(["GET", "POST"])
def ManagersView(request):
    return UsersView(request, role="manager")


@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
@api_view(["GET", "PUT", "PATCH", "DELETE"])
def ManagerView(request, id):
    return UserView(request, id, role="manager")


@authentication_classes([TokenAuthentication])
@permission_classes([IsEmployeeOrReadOnly])
@api_view(["GET", "POST"])
def CustomersView(request):
    return UsersView(request, role="customer")


@authentication_classes([TokenAuthentication])
@permission_classes([IsEmployeeOrReadOnly])
@api_view(["GET", "PUT", "PATCH", "DELETE"])
def CustomerView(request, id):
    return UserView(request, id, role="customer")
