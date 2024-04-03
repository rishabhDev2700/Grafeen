from django.shortcuts import redirect, render
from django.contrib import messages
from store.forms import DiscountForm, ProductForm
from store.models import Discount, Product


# Create your views here.
def seller_dashboard(request):
    return render(request, "dashboard/seller_dashboard.html")


def buyer_dashboard(request):
    return render(request, "dashboard/buyer_dashboard.html")


def add_product(request):
    if request.method == "POST":
        data = request.POST.copy()
        data.update({"owner": request.user.id})
        form = ProductForm(data, request.FILES)
        if form.is_valid():
            print("Product added successfully")
            form.save()
            messages.success(request, "Product Added Successfully")
            return redirect("account:my-account")
    form = ProductForm()
    return render(request, "dashboard/form.html", {"form": form, "item": "Product"})


def add_discount(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
            messages.success(request, "Discount Added Successfully")

            return redirect("account/my-account")
    form = DiscountForm()
    return render(request, "dashboard/form.html", {"form": form, "item": "Discount"})


def my_products(request):
    products = Product.objects.filter(owner=request.user, is_available=True)
    return render(request, "dashboard/list.html", {"items": products})


def my_discounts(request):
    discounts = Discount.objects.filter(product__owner=request.user)
    return render(request, "dashboard/list.html", {"items": discounts})


def update_product(request, pk):
    product = Product.objects.get(pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Update Successfully")
            return redirect("dashboard:my-account")
        else:
            messages.error(request, "Some Error Occurred!!")
    form = ProductForm(instance=product)
    return render(request, "dashboard/form.html", {"form": form})


def update_discount(request, pk):
    discount = Discount.objects.get(pk=pk)
    if request.method == "POST":
        form = DiscountForm(request.POST, instance=discount)
        if form.is_valid():
            form.save()
            messages.success(request, "Discount Update Successfully")
            return redirect("account:my-account")
        else:
            messages.error(request, "Some Error Occurred!!")
    form = DiscountForm(instance=discount)
    return render(request, "dashboard/form.html", {"form": form})


def delete_product(request):
    product_id = request.POST["product_id"]
    try:
        product = Product.objects.get(pk=product_id)
        product.delete()
        messages.success(request, "Product deleted Successfully")
    except:
        messages.error(request, "Some Error Occurred")
    return redirect("account/my-account")


def delete_discount(request):
    discount_id = request.POST["discount_id"]
    try:
        discount = Product.objects.get(pk=discount_id)
        discount.delete()
        messages.success(request, "Discount deleted Successfully")
    except:
        messages.error(request, "Some Error Occurred")
    return redirect("account/my-account")
