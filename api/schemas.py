from ninja import ModelSchema

from account.models import User
from store.models import Discount, Product

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['email','is_seller',"full_name"]


class ProductInfo(ModelSchema):
    class Meta:
        model = Product
        fields = ['name',"description","slug","category","price"]
    
class DiscountSchema(ModelSchema):
    class Meta:
        model = Discount
        fields = ['product','percentage','name','valid_till']