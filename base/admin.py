from django.contrib import admin
from .models import User
from .profiles import ManagerProfile, EmployeeProfile, CustomerProfile
from .models import Category, Product, ProductGallery ,CartItem
from import_export import resources
from import_export.admin import ImportExportModelAdmin

admin.site.register(User)
admin.site.register(ManagerProfile)
admin.site.register(EmployeeProfile)
admin.site.register(CustomerProfile)

admin.site.register(Category)
admin.site.register(CartItem)

# -------- PRODUCT GALLERY -------- #
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 3 
    fields = ['product', 'image']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'photo')
    inlines = [ProductGalleryInline]


admin.site.register(ProductGallery)