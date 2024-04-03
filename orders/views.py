from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from orders.cart import Cart
from store.models import Order, OrderProduct
from store.models import Product
import razorpay
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from config import settings
from store.models import Order, OrderProduct
from orders.models import PaymentOrder


# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    context = {"cart": cart, "subtotal": cart.__len__()}
    return render(request, "orders/cart_summary.html", context=context)


def cart_add(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product)
        cart_quantity = cart.__len__()
        response = JsonResponse(
            {"quantity": cart_quantity, "message": f"{product.name} added"}
        )
        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get("action") == "post":
        product_id = int(request.POST.get("product_id"))
        product = get_object_or_404(Product, id=product_id)
        cart.delete(product=product)
        cart_quantity = cart.__len__()
        cart_subtotal = cart.get_subtotal()
        response = JsonResponse(
            {
                "quantity": cart_quantity,
                "subtotal": cart_subtotal,
                "message": f"{product.name} removed",
            }
        )
        return response


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return JsonResponse({"quantity": 0, "subtotal": 0, "message": "Cart Cleared"})


def view_orders(request):
    all_orders = Order.objects.filter(user=request.user)
    incompleted = all_orders.filter(is_completed=False)
    incompleted_orders = []
    for order in incompleted:
        items = OrderProduct.objects.filter(order=order)
        incompleted_orders.append([order, items])
    completed = all_orders.filter(is_completed=True)
    completed_orders = []
    for order in completed:
        items = OrderProduct.objects.filter(order=order)
        completed_orders.append([order, items])
    context = {
        "completed_orders": completed_orders,
        "incompleted_orders": incompleted_orders,
    }
    return render(request, "orders/view_orders.html", context=context)


client = razorpay.Client(auth=(settings.RAZORPAY_KEY, settings.RAZORPAY_SECRET))


def create_payment_order(request):
    amount = int(Cart(request).get_subtotal().__str__())
    if amount < 10:
        messages.error(request, "Total Amount should be greater than or equal to 10!")
        return redirect("orders:summary")
    razorpay_order = client.order.create(
        dict(amount=(amount * 100), currency="INR", payment_capture="0")
    )
    payment_order = PaymentOrder(
        user=request.user,
        payment_order_id=razorpay_order["id"],
        amount=amount,
    )
    payment_order.save()
    callback_url = "paymenthandler/"
    context = {
        "razorpay_order_id": razorpay_order["id"],
        "razorpay_merchant_key": settings.RAZORPAY_KEY,
        "razorpay_amount": (amount * 100),
        "currency": "INR",
        "callback_url": callback_url,
    }
    return render(request, "orders/checkout.html", context=context)


# noinspection PyBroadException
@csrf_exempt
def payment_handler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST["razorpay_payment_id"]
            order_id = request.POST["razorpay_order_id"]
            signature = request.POST["razorpay_signature"]
            data = {
                "razorpay_payment_id": payment_id,
                "razorpay_order_id": order_id,
                "razorpay_signature": signature,
            }
            result = client.utility.verify_payment_signature(data)
            if result is not None:
                try:
                    payment_order = PaymentOrder.objects.get(payment_order_id=order_id)
                    client.payment.capture(payment_id, payment_order.amount * 100)
                    order = Order.objects.create(
                        user=request.user,
                        total=payment_order.amount,
                        razorpay_order_id=order_id,
                    )
                    payment_order.order = order
                    payment_order.payment_id = payment_id
                    payment_order.signature = signature
                    payment_order.verified = True
                    payment_order.save()
                    cart = Cart(request)
                    for item in cart:
                        OrderProduct.objects.create(
                            order=order, product=item["product"], price=item["price"]
                        )
                    messages.success(request, "Order placed Successfully")
                    return redirect("orders:download", order.id)
                except RuntimeError as e:
                    messages.error(request, "Payment Completed\t", e)
            else:
                messages.error(request, "Order Failed. Not verified!!")
        except:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


def downloads(request, id):
    order = Order.objects.get(id=id)
    orderProducts = OrderProduct.objects.filter(order=order)
    print(orderProducts)
    return render(request, "orders/downloads.html", {"products": orderProducts})
