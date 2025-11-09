from django.urls import path
from . import views

urlpatterns = [
  path('', views.getRoutes),
  path('products/', views.getProducts),
  path('products/<str:id>/', views.getProduct),
  path('employees/', views.getEmployees),
  path('managers', views.getManagers),
  path('customers', views.getCustomers),
  path('employees/<str:id>/', views.getEmployee),
  path('managers/<str:id>/', views.getManager),
  path('customers/<str:id>/', views.getCustomer),
]