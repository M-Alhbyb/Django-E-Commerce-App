from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
  
  #path('login/', views.testview , name='login'),
  #path('logout/', views.testview, name='logout'), 
  # path('redirect/', views.user_redirect, name='redirect'),  
  
  # pages
  path('', views.home, name='home'),  
  path('all/', views.all_products, name='all-products'),
  path('categories/<str:category_name>', views.category_products, name='categories'),
  path('deals/', views.hot_deals, name='hot-deals'),
  path('profile/<str:id>', views.profile, name='profile'),
  
  # --------
  path('cart/<str:id>', views.cart, name='cart'),
  
  # manage cart
  path('add-to-cart/<str:id>', views.add_to_cart, name='add-to-cart'),
  path('delete-from-cart/<str:id>', views.delete_from_cart, name='delete-from-cart'), 
  path('checkout/<str:id>', views.checkout, name='checkout'),
  
  path('product/<str:id>', views.product_view, name='product'),

  path('test/', views.test_view, name='test') 
  # Manage Users 
 # path('manager/<str:id>', views.manage_employees, name='manager'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)