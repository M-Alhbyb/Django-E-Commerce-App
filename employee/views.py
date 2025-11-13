from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from base.models import Product, ProductGallery, Category
from .forms import CreateProductForm
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from base.decorators import allowed_roles
from django.http import HttpResponse
from base.models import Product
from .resources import ProductResource

def _total(model, field):
    return model.objects.aggregate(total=Sum(field))["total"] or 0


@login_required(login_url='account_login')
@allowed_roles(['employee'])
def home(request):
    total_sales = _total(Product, "sales_count")
    total_stock = _total(Product, "stock")
    total_price = _total(Product, "price")
    total_products = Product.objects.count()
    
    context = {
        "no_search_bar": True,
        "total_sales": total_sales,
        "total_stock": total_stock,
        "total_price": total_price,
        "total_products": total_products,
        "products": Product.objects.all(),
        "categories": Category.objects.all()
    }
    return render(request, "employee/index.html", context)


@login_required(login_url='account_login')
@allowed_roles(['employee'])
def createProduct(request):
    form = CreateProductForm()
    if request.method == "POST":
        form = CreateProductForm(request.POST, request.FILES)
        images = request.FILES.getlist("images")
        if form.is_valid():
            product = form.save()
            for image in images:
                ProductGallery.objects.create(product=product, image=image)
            return redirect("employee:home")
        messages.error(request, "Data is not valid, Try Again!")

    context = {"no_search_bar": True, "form": form}
    return render(request, "employee/add-update-product.html", context)


@login_required(login_url='account_login')
@allowed_roles(['employee'])
def updateProduct(request, id):
    product = get_object_or_404(Product, id=id)
    form = CreateProductForm(instance=product)
    if request.method == "POST":
        form = CreateProductForm(request.POST, request.FILES, instance=product)
        images = request.FILES.getlist("images")
        if form.is_valid():
            product = form.save()
            for image in images:
                ProductGallery.objects.create(product=product, image=image)
            return redirect("employee:home")
        messages.error(request, "Data is not valid, Try Again!")
    #
    return render(request, "employee/add-update-product.html", {"no_search_bar": True, "form": form, 'update':'update'})

def viewProduct(requset, id):
    return redirect('product', id=id)

@login_required(login_url='account_login')
@allowed_roles(['employee'])
def deleteProduct(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        messages.success(request, f'Product {product.name} Deleted Successfully!')
        product.delete()
        return redirect('employee:home')

    return render(request, 'employee/delete-product.html', {"product": product})




from itertools import groupby
from operator import attrgetter # Useful for keying by model attribute

@login_required
@allowed_roles(['employee'])
def viewProducts(request):
    products = Product.objects.all().order_by('category', 'name')
    if request.method == 'GET':
        q = request.GET.get('q')
        if q != None:
            products = Product.objects.filter(name__icontains=q)
    
    grouped_products = {}    
    for category, product_group in groupby(products, key=attrgetter('category')):
        grouped_products[category] = list(product_group)
    
    context = {
        'grouped_products': grouped_products, 
        'page_title': 'Inventory by Category',
        'current_view': 'all-products' 
    }
    
    return render(request, 'employee/product_list.html', context)



@login_required
@allowed_roles(['employee'])
def export_products(request):
    resource = ProductResource()
    
    dataset = resource.export()
    
    xlsx_content = dataset.export('xlsx')
    
    response = HttpResponse(
        xlsx_content, 
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
    )
    
    response['Content-Disposition'] = 'attachment; filename="products.xlsx"'
    return response