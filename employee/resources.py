from import_export import resources
from base.models import Product

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        # optional: fields you want to include/exclude
        # fields = ('id', 'title', 'author',)