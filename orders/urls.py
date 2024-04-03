from django. urls import path
from orders import views
app_name = "orders"
urlpatterns = [
    path("summary/", views.cart_summary, name="summary"),
    path("add/", views.cart_add, name="cart_add"),
    path("delete/", views.cart_delete, name="cart_delete"),
    path("clear/", views.cart_clear, name="cart_clear"),
    path("orders/", views.view_orders, name="view_orders"),
    path("", views.create_payment_order, name="create_payment"),
    path("paymenthandler/", views.payment_handler, name="payment_handler"),
    path("downloads/<int:id>", views.downloads, name="download")
]
