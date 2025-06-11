from django import forms
from .models import Product,ProductImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image','alt_text','is_featured']


