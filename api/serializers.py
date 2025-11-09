from rest_framework import serializers
from base.models import Product, ProductGallery, User
from base.profiles import EmployeeProfile, ManagerProfile, CustomerProfile

class ProductGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGallery
        exclude = ['product']  

class ProductSerializer(serializers.ModelSerializer):
    gallery = ProductGallerySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        exclude = ['updated_at']  



class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerProfile
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        exclude = ['id', 'user']  

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = ['phone_number', 'address', 'date_hired', 'department', 'position', 'salary']


class UserSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'email', 'photo', 'role', 'profile'
        ]

    def get_profile(self, obj):
        if obj.role == 'employee' and hasattr(obj, 'employeeprofile'):
            return EmployeeSerializer(obj.employeeprofile).data
        elif obj.role == 'manager' and hasattr(obj, 'managerprofile'):
            return ManagerSerializer(obj.managerprofile).data
        elif obj.role == 'customer' and hasattr(obj, 'customerprofile'):
            return CustomerSerializer(obj.customerprofile).data
        return None