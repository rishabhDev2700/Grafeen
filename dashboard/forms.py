from django.forms import modelformset_factory
from django.forms import ModelForm
from store.models import ProductImage

class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = ('name','url','product')



ProductImagesFormset = modelformset_factory(ProductImage,ProductImageForm)