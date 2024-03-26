from typing import List
from django.shortcuts import get_object_or_404
from ninja.security import django_auth
from ninja_extra import NinjaExtraAPI
from api.schemas import ProductInfo, UserSchema
from store.models import Category, Product
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_jwt.authentication import JWTAuth
app = NinjaExtraAPI(auth=JWTAuth())
app.register_controllers(NinjaJWTDefaultController)
# get all products of a seller
@app.get("/all-products",response=List[ProductInfo])
def all_products(request):
    products = Product.objects.filter(owner=request.user)
    return products

# get all orders of a seller

# add product
@app.post("add-product/")
def add_product(request,product:ProductInfo):
    category:Category = get_object_or_404(Category,id=product.category)
    product.category = category
    product = Product.objects.create(**product.dict(),owner=request.user)
    return {"id":product.id}
    