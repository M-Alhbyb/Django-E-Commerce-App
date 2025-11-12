from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import User, Category, Product, ProductGallery, Cart, CartItem
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from base.decorators import allowed_roles

def testview(request):
    form = LoginForm()
    context = {
        'form':form
    }
    return render(request, 'base/test.html')

def loginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        userAuth = authenticate(request, username=username, password=password)
        if userAuth:
            login(request, userAuth)
            user = User.objects.get(username=username)
            return user_redirect(user)
        else:
            messages.error(request, "Username or password is incorrect")

    return render(request, "base/login.html")


def user_redirect(user):
    if user.role == "manager":
        url = reverse("manager:home")
        return redirect(url)
    elif user.role == "employee":
        url = reverse("employee:home")
        return redirect(url)
    else:
        return redirect("home")


def home(request):
    products = Product.objects.all()
    filtered = products
    if request.GET:
        select = request.GET.get("s")
        query = request.GET.get("q")

        if select == "all":
            filtered = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        else:
            filtered = Product.objects.filter(
                Q(category=select)
                & Q(Q(name__icontains=query) | Q(description__icontains=query))
            )

    categories = Category.objects.all()
    for category in categories:
        category.image_filename = f"img/shop-{category}.png"

    hot_deals = filtered.filter(is_hot_deal=True)[:8]
    new_products = filtered.order_by("-created_at")[:8]
    top_sellings = filtered.order_by("-sales_count")
    context = {
        "products": filtered,
        "categories": categories,
        "hot_deals": hot_deals,
        "new_products": new_products,
        "top_sellings": top_sellings,
    }

    if request.user.id != None:
        if request.user.role in ['manager', 'employee']:
            return user_redirect(request.user)

        user = User.objects.get(id=request.user.id)
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = []
        for item in CartItem.objects.all():
            if item.cart == cart:
                cart_items.append(item)

        total_price = 0
        for item in CartItem.objects.all():
            total_price += item.product.price * item.quantity

        context["user"] = user
        context["cart"] = cart
        context["cart_items"] = cart_items
        context["total_price"] = total_price
        return render(request, "base/index.html", context)

    return render(request, "base/index.html", context)


def all_products(request):
    user = request.user
    filtered = Product.objects.all()

    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = []
    for item in CartItem.objects.all():
        if item.cart == cart:
            cart_items.append(item)

    if request.GET:
        select = request.GET.get("s")
        query = request.GET.get("q")
        filtered = Product.objects.filter(
            Q(Q(name__icontains=query) | Q(description__icontains=query))
        )

    context = {
        "user": user,
        "categories": Category.objects.all,
        "cart": cart,
        "cart_items": cart_items,
        "products": filtered,
    }

    return render(request, "base/categories.html", context)

def category_products(request, category_name):
    context = {}
    if request.user.id != None:
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = []
        for item in CartItem.objects.all():
            if item.cart == cart:
                cart_items.append(item)
        
        context["user"] = user
        context["cart"] = cart
        context["cart_items"] = cart_items

    category = get_object_or_404(Category, name__iexact=category_name)
    filtered = Product.objects.filter(category=category)



    if request.GET:
        select = request.GET.get("s")
        query = request.GET.get("q")
        filtered = Product.objects.filter(
            Q(category=category)
            & Q(Q(name__icontains=query) | Q(description__icontains=query))
        )

    context = {
        "category": category,
        "products": filtered,
    }

    return render(request, "base/categories.html", context)


def hot_deals(request):
    user = request.user
    filtered = Product.objects.filter(is_hot_deal=True).order_by("-discount")
    cart = get_object_or_404(Cart, user=user)
    if request.GET:
        select = request.GET.get("s")
        query = request.GET.get("q")
        filtered = Product.objects.filter(
            Q(is_hot_deal=True)
            & Q(Q(name__icontains=query) | Q(description__icontains=query))
        )

    context = {
        "user": user,
        "cart": cart,
        "products": filtered,
    }

    return render(request, "base/deals.html", context)


@login_required(login_url='account_login')
@allowed_roles(['customer'])
def cart(request, id):
    user = get_object_or_404(User, id=id)
    cart = get_object_or_404(Cart, user=user)
    if request.user != user:
        return HttpResponse("Access Denied")

    total_price = 0
    for item in CartItem.objects.all():
        total_price += item.product.price * item.quantity
    context = {
        "cart": cart,
        "products": cart.products.all(),
        "total_price": total_price,
        "no_search_bar": "no",
    }
    return render(request, "base/cart.html", context)

@login_required(login_url='account_login')
@allowed_roles(['customer'])
def add_to_cart(request, id):
    cart = get_object_or_404(Cart, user=request.user)
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        quantity = request.POST.get("quantity")
        if CartItem.objects.create(cart=cart, product=product, quantity=quantity):
            messages.success(request, f" {product} Added To Cart!")
        else:
            messages.error(request, "Item Didn't Added, Try Again!")

        # return redirect(request.META.get('HTTP_REFERER', '/'))
        return redirect("home")

    context = {
        "no_search_bar": "no",
        "user": request.user,
        "cart": cart,
        "product": product,
    }
    return render(request, "base/add_to_cart.html", context)


@login_required(login_url='account_login')
@allowed_roles(['customer'])
def delete_from_cart(request, id):
    product = get_object_or_404(Product, id=id)
    for item in CartItem.objects.all():
        if item.product == product:
            item.delete()
    messages.error(request, f"{product} Deleted From Cart!")
    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required(login_url='account_login')
@allowed_roles(['customer'])
def profile(request, id):
    user = get_object_or_404(User, id__iexact=id)
    cart = get_object_or_404(Cart, user=user)

    if request.user.id != user.id:
        return HttpResponse("Access Denied")

    total_price = 0
    for item in CartItem.objects.all():
        total_price += item.product.price * item.quantity

    cart_items = []
    for item in CartItem.objects.all():
        if item.cart == cart:
            cart_items.append(item)

    context = {
        "no_search_bar": "no",
        "user": user,
        "cart": cart,
        "cart_items": cart_items,
        "total_price": total_price,
    }

    return render(request, "base/profile.html", context)


@login_required(login_url='account_login')
@allowed_roles(['customer'])
def checkout(request, id):
    user = get_object_or_404(User, id=id)
    cart = get_object_or_404(Cart, user=user)
    if request.user != user:
        return HttpResponse("Access Denied")

    total_price = 0
    for item in CartItem.objects.all():
        total_price += item.product.price * item.quantity

    cart_items = []
    for item in CartItem.objects.all():
        if item.cart == cart:
            cart_items.append(item)

    context = {"cart": cart, "cart_items": cart_items, "total_price": total_price}
    return render(request, "base/checkout.html", context)


def product_view(request, id):
    context = {}
    if request.user.id != None:
        user = request.user

        # FOR CART SHOWING IN HEADER
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = []
        for item in CartItem.objects.all():
            if item.cart == cart:
                cart_items.append(item)

        total_price = 0
        for item in CartItem.objects.all():
            total_price += item.product.price * item.quantity
        # ----------------------------
        context["user"]= user,
        context["cart"]= cart,
        context["cart_items"]= cart_items,
        context["total_price"]= total_price,
    product = get_object_or_404(Product, id=id)
    gallery = product.gallery.all()
    gallery_couunt = product.gallery.count()

    related_products = Product.objects.filter(category=product.category).order_by(
        "-discount"
    )[:4]


    context = {
        "no_search_bar": "no",
        "product": product,
        "related_products": related_products,
        "gallery": gallery,
        "gallery_count": gallery_couunt,
    }

    return render(request, "base/product_page.html", context)
