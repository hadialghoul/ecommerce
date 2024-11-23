from django.shortcuts import render
from store.models import Category,Product
from django.shortcuts import get_object_or_404

# Create your views here.
def store(request):
    all_products=Product.objects.all()
    context={'my_products':all_products}
    return render(request,'store/store.html',context)


def categories(request):
    all_categories=Category.objects.all()
    return {'all_categories':all_categories}


def product_info(request,slug):
    product=get_object_or_404(Product,slug=slug)
    context={'product':product}
    return render(request,'store/product-info.html',context)


def category_list(request,slug):
    category=get_object_or_404(Category,slug=slug)
    
    return render(request,'store/list-category.html',{'category':category})




