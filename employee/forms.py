from base.models import Product, ProductGallery
from django import forms

class CreateProductForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = '__all__'
# 
class CreateGalleryForm(forms.ModelForm):
  class Meta:
    model = ProductGallery
    fields = ['product','image']
