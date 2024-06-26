"""This file contains all view functions related to store"""

from django.shortcuts import redirect, render, get_object_or_404
from store.forms import RatingForm
from store.models import Category, Product, Rating
from django.db.models import Prefetch
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector

# Create your views here.


def homepage(request):
    """
    Home page of the website
    """
    new_arrivals = Product.objects.all()[:10]
    context = {"new_arrivals": new_arrivals}
    return render(request, "store/homepage.html", context=context)


def explore(request):
    """
    Explore page of the website
    """
    categories = Category.objects.prefetch_related(
        Prefetch(
            "product_set",
            queryset=Product.objects.filter(is_available=True)[:4],
            to_attr="limited_products",
        )
    ).all()
    return render(request, "store/explore.html", context={"categories": categories})


def list_all(request):
    """
    Shows all products available
    """
    # todo: add pagination
    products = Product.objects.filter(is_available=True)
    paginator = Paginator(products, 8)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {"products": page}
    return render(request, "store/list-all.html", context=context)


def show_product(request, slug):
    """Show a particular product"""
    product = get_object_or_404(Product, slug=slug)
    reviews = Rating.objects.filter(product=product)[:5]
    context = {"product": product, "reviews": reviews}
    return render(request, "store/show-product.html", context=context)


def list_categories(request):
    """
    Shows the list of categories
    """
    categories = Category.objects.all()
    context = {"categories": categories}
    return render(request, "store/list-categories.html", context=context)


def show_category(request, slug):
    """Shows all products in the given category"""
    category = get_object_or_404(
        Category.objects.prefetch_related("product_set"), slug=slug
    )
    categories = Category.objects.all()
    products = category.product_set.filter(is_available=True)
    context = {
        "category": category,
        "products": products,
        "categories": categories,
    }
    return render(request, "store/show-category.html", context=context)


def list_best_sellers(request):
    """Fetches the bestsellers"""
    return render(request, "store/list-best-sellers.html")


def list_new_arrivals(request):
    """Fetches the new arrivals from the database"""
    return render(request, "store/list-new-arrivals.html")


def landing(request):
    return render(request, "store/landing_page.html")


def review_form(request, id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        data = request.POST.copy()
        # data.update({"product__id"})
        form = RatingForm(data=data)
        if form.is_valid():
            form.save()
            return redirect("store:show-product", product.slug)
        else:
            return render(request, "store/review-page.html", context={"form": form})
    form = RatingForm(data={"product": product, "user": request.user})
    return render(
        request, "store/review-page.html", context={"form": form, "product": product}
    )


def search_products(request):
    query = request.GET.get("query")
    search_result = Product.objects.annotate(
        search=SearchVector("name", "description", "slug")
    ).filter(search=query)
    print(search_result)
    return render(
        request, "store/search-products.html", context={"products": search_result}
    )
