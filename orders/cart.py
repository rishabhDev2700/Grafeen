from decimal import Decimal

from config import settings
from store.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if settings.CART_SESSION_ID not in request.session:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        self.cart[product_id] = {'price': str(product.price)}
        self.save()

    # Not needed
    def delete(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.cart_SESSION_ID]

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for product in cart.values():
            product['price'] = Decimal(product['price'])
            yield product

    def __len__(self):
        return len(self.cart.values())

    def get_subtotal(self):
        return sum(Decimal(product['price']) for product in self.cart.values())

    def save(self):
        self.session.modified = True