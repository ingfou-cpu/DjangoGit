from .cart import Cart

# Ajouter le panier au contexte de la requête
# create a context processor so our cart work throughout the site (all pages)
def cart(request):
    return {'cart': Cart(request)}
    
