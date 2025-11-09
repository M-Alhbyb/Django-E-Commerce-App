from django.urls import path
from . import views

app_name = 'employee'

urlpatterns = [
    path('', views.home, name='home'),
    path('product/create', views.createProduct, name='create-product'),
    path('product/<str:id>/update', views.updateProduct, name='update-product'),
    path('product/<str:id>/view', views.viewProduct, name='view-product'),
    path('product/<str:id>/delete', views.deleteProduct, name='delete-product'),
    path('products/all', views.viewProducts, name='all-products'),
    path('products/export', views.export_products, name='export-products'),
]
