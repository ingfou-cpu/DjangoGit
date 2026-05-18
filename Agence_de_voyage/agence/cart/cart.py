from decimal import Decimal


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, product, quantity=1, product_type='destination'):
        """
        Add a product to the cart.
        product_type can be: 'destination', 'pack_travel', 'hotel'
        """
        product_id = str(product.id)
        key = f"{product_type}_{product_id}"

        if key in self.cart:
            self.cart[key]['quantity'] += quantity
        else:
            self.cart[key] = {
                'quantity': quantity,
                'name': str(product.name) if hasattr(product, 'name') else str(product.pack_name),
                'price': str(product.price),
                'product_type': product_type,
                'product_id': product_id,
            }
        self.session.modified = True

    def remove(self, product_key):
        """Remove a product from the cart by its key."""
        if product_key in self.cart:
            del self.cart[product_key]
            self.session.modified = True

    def __iter__(self):
        """Iterate over cart items and add computed fields."""
        for key, item in self.cart.items():
            item['total_price'] = Decimal(item['price']) * item['quantity']
            item['key'] = key
            yield item

    def __len__(self):
        """Count all items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Get the total price of all items in the cart."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Clear the cart."""
        self.session['session_key'] = {}
        self.session.modified = True

    def save(self):
        self.session.modified = True
