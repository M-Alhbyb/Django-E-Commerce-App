from rest_framework import serializers
from base.models import Product, ProductGallery, User
from base.profiles import EmployeeProfile, ManagerProfile, CustomerProfile
from django.http import HttpResponse

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
    
    def create(self, data): 
        profile_data = self.initial_data.get('profile', None)
        role = self.initial_data.get('role', None)
        user = User.objects.create(**data)
        if profile_data:
            userProfile = object
            
            if role == 'employee':
                userProfile = EmployeeProfile.objects.get(user=user)  
            elif role == 'manager':
                userProfile = ManagerProfile.objects.get(user=user)  
            if role == 'customer':
                userProfile = CustomerProfile.objects.get(user=user)  

            for item in profile_data:
                setattr(userProfile, item, profile_data[item])
            userProfile.save()
        return user
   
    def update(self, instance, validated_data):
        profile_data = self.initial_data.get('profile', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if profile_data:
            if instance.role == 'employee':
                EmployeeProfile.objects.update_or_create(user=instance, defaults=profile_data)
            elif instance.role == 'manager':
                ManagerProfile.objects.update_or_create(user=instance, defaults=profile_data)
            elif instance.role == 'customer':
                CustomerProfile.objects.update_or_create(user=instance, defaults=profile_data)

        return instance



