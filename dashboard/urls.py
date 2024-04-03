from django.urls import path

from dashboard.views import add_discount, add_product, update_product,update_discount,delete_product,my_discounts,my_products,delete_product,delete_discount

app_name = "dashboard"
urlpatterns = [
    path('add-product',add_product,name="add-product"),
    path('update-product',update_product,name="update-product"),
    path('delete-product',delete_product,name="delete-product"),
    path('my-products',my_products,name="my-products"),
    path('add-discount',add_discount,name="add-discount"),
    path('update-discount',update_discount,name="update-discount"),
    path('delete-discount',delete_discount,name="delete-discount"),
    path('my-discounts',my_discounts,name="my-discounts"),
]