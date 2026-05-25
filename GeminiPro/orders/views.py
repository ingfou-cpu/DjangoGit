from django.shortcuts import render, redirect
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # clear the cart
            cart.clear()
            # Send mock email
            send_mail(
                'Order Confirmation',
                f'Dear {order.first_name}, your order has been placed successfully. Order ID: {order.id}',
                'noreply@eshop.com',
                [order.email],
                fail_silently=False,
            )
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        # Pre-fill form with user info if available
        form = OrderCreateForm(initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email
        })
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})
