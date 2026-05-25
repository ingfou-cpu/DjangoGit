from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Review, Wishlist
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)
        
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'products/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    reviews = product.reviews.all()
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
        messages.success(request, 'Review added successfully.')
        return redirect(product.get_absolute_url())
    
    return render(request, 'products/product/detail.html', {
        'product': product,
        'reviews': reviews
    })

@login_required
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'products/wishlist.html', {'wishlist': wishlist})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    messages.success(request, f'{product.name} added to your wishlist.')
    return redirect('products:wishlist')
