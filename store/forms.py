from django import forms
from store.models import Discount, Product, Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["rating", "review", "product", "user"]
        widgets = {
            "rating": forms.TextInput(
                attrs={
                    "type": "range",
                    "min": "0",
                    "max": "5",
                    "list": "rating",
                }
            ),
            "product": forms.TextInput(attrs={"readonly": "true"}),
            "user": forms.TextInput(attrs={"hidden": "true"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "cover", "slug", "price", "category", "tags"]


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ["percentage", "name", "valid_till"]
