from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from Agapp.models import Destination, pack_travel, Hotel
from django.http import JsonResponse


def cart_summary(request):
    cart = Cart(request)
    return render(request, "cart_summary.html", {'cart': cart})


def add_cart(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_type = request.POST.get('product_type', 'destination')
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity', 1))

        if product_type == 'pack_travel':
            product = get_object_or_404(pack_travel, id=product_id)
            product_name = str(product.pack_name)
        elif product_type == 'hotel':
            product = get_object_or_404(Hotel, id=product_id)
            product_name = str(product.hotel_name)
        else:
            product = get_object_or_404(Destination, id=product_id)
            product_name = str(product.name)

        cart.add(product=product, quantity=quantity, product_type=product_type)

        response = JsonResponse({
            'product_name': product_name,
            'quantity': quantity
        })
        return response

    return redirect('cart_summary')


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_key = request.POST.get('product_key')
        cart.remove(product_key)
        response = JsonResponse({'deleted': product_key})
        return response
    return redirect('cart_summary')


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_key = request.POST.get('product_key')
        quantity = int(request.POST.get('quantity', 1))
        if product_key in cart.cart:
            cart.cart[product_key]['quantity'] = quantity
            cart.save()
            response = JsonResponse({'updated': product_key, 'quantity': quantity})
            return response
    return redirect('cart_summary')
