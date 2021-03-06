from django.shortcuts import render, get_object_or_404, redirect
from .forms import CartAddProductForm
from .cart import Cart
from shop.models import Product
from django.views.decorators.http import require_POST
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    forms = CartAddProductForm(request.POST)
    if forms.is_valid():
        cd = forms.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_item'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    coupon_apply_form = CouponApplyForm()
    r = Recommender()
    recommended_products = None
    cart_products = [ item['product'] for item in cart]
    if cart_products:
        recommended_products = r.suggest_products_for(cart_products, max_result=8)
    return render(request, 'cart/detail.html', {'cart': cart, 'coupon_apply_form': coupon_apply_form, 'recommended_products': recommended_products})

