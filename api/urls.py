from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
  path('', views.getRoutes),
  
  # PRODUcTS
  path('products/', views.ProductsView),
  path('products/<str:id>/', views.ProductView),
  
  # GET ALL
  path('employees/', views.EmployeesView),
  path('managers', views.ManagersView),
  path('customers', views.CustomersView),
  
  #GET ONE
  path('employees/<str:id>/', views.EmployeeView),
  path('managers/<str:id>/', views.ManagerView),
  path('customers/<str:id>/', views.CustomerView),

  # Get Token  
  path('auth/token/', obtain_auth_token, name='api_token_auth'), 
]