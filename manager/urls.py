from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'manager'

urlpatterns = [
  path('', views.home, name='home'),  
  path('employee/create', views.addEmployee, name='create-employee'),  
  path('employee/<str:id>/view', views.viewEmployee, name='view-employee'),  
  path('employee/<str:id>/edit', views.updateEmployee, name='edit-employee'),  
  path('employee/<str:id>/delete', views.deleteEmployee, name='delete-employee'),  
  path('employees/', views.allEmployees, name='all-employees'),  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)