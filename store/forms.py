from django.forms import ModelForm, TextInput

from store.models import Rating

class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['rating','review']
        widgets = {
            "rating":TextInput(attrs={"type":"range","min":"0","max":"5", "list":"rating"
            })
        }