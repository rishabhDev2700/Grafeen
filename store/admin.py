from django.contrib import admin

from store.models import Category, Discount, Order, OrderProduct, Product, ProductImage, Rating

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Discount)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Rating)