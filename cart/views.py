from django.shortcuts import render
from .cart import Cart
from django.shortcuts import get_object_or_404
from store.models import Product
from django.http import JsonResponse


# Create your views here.
def cart_summary(request):
    cart=Cart(request)
    return render(request,'cart/cart-summary.html',{'cart':cart})

def cart_add(request):
    cart=Cart(request)#fat7na session
    if request.POST.get('action')=='post': #eza laction bel ajax heye post
        product_id=int(request.POST.get('product_id')) #lproduct id min lajax lbel frontend
        product_quantity=int(request.POST.get('product_quantity'))# lproduct quntity lbel ajax
        product=get_object_or_404(Product,id=product_id)#product min ldatabase bas id=id to3ol lfrontend lb2lb lvalue
        cart.add(product=product,product_qty=product_quantity)# mn5od lproduct lmin database w qunatity min ajax w mn3ml add function bel cart.py
        cart_quantity=cart.__len__()
        response=JsonResponse({'qty':cart_quantity})
        return response





def cart_delete(request):

    cart = Cart(request)

    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)


        cart_quantity = cart.__len__()

        cart_total = cart.get_total()


        response = JsonResponse({'qty':cart_quantity, 'total':cart_total})

        return response



def cart_update(request):

    cart = Cart(request)

    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        cart.update(product=product_id, qty=product_quantity)


        cart_quantity = cart.__len__()

        cart_total = cart.get_total()


        response = JsonResponse({'qty':cart_quantity, 'total':cart_total})

        return response
