from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from base.models import Product
from .resources import ProductResource

class ProductAdmin(ImportExportModelAdmin):
    resource_classes = [ProductResource]