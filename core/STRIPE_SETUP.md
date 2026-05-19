# Configuration du Système de Paiement Stripe

## Installation

Les dépendances suivantes ont été installées :
- `stripe` - Bibliothèque officielle Stripe
- `python-dotenv` - Gestion des variables d'environnement

## Structure du Projet

```
sim/
├── models.py          # Modèles Product, CheckoutSessionRecord, PaymentHistory
├── views.py           # Vues pour le checkout, webhook, historique
├── urls.py            # Routes URL
├── admin.py           # Configuration de l'administration
└── templates/
    ├── home.html              # Page d'accueil avec liste des produits
    ├── success.html           # Page de succès après paiement
    ├── cancel.html            # Page d'annulation
    └── payment_history.html   # Historique des paiements
```

## Configuration

### 1. Clés API Stripe

Les clés sont configurées dans `core/.env` :

```env
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### 2. Créer des Produits dans Stripe

1. Connectez-vous à votre [Dashboard Stripe](https://dashboard.stripe.com)
2. Allez dans **Produits** → **Ajouter un produit**
3. Créez un produit avec un prix
4. Récupérez le **Price ID** (commence par `price_`)

### 3. Ajouter des Produits dans Django

1. Lancez le serveur : `python manage.py runserver`
2. Allez dans l'administration : `http://127.0.0.1:8000/admin/`
3. Connectez-vous avec un superutilisateur
4. Ajoutez un produit avec :
   - Nom
   - Description
   - Prix (en euros)
   - Stripe Price ID (ex: `price_1234567890`)

### 4. Configurer le Webhook (pour la production)

1. Dans Stripe Dashboard, allez dans **Developers** → **Webhooks**
2. Ajoutez un endpoint : `https://votre-domaine.com/webhook/`
3. Sélectionnez les événements :
   - `checkout.session.completed`
   - `checkout.session.expired`
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`
   - `charge.refunded`
4. Récupérez le **Signing Secret** et ajoutez-le dans `.env`

### 5. Tester en Mode Test

Utilisez les cartes de test Stripe :
- **Succès** : `4242 4242 4242 4242`
- **Échec** : `4000 0000 0000 0002`
- N'importe quelle date d'expiration future et CVC

## URLs Disponibles

| URL | Description |
|-----|-------------|
| `/` | Page d'accueil avec produits |
| `/checkout/<product_id>/` | Créer une session de paiement |
| `/success/` | Page de succès |
| `/cancel/` | Page d'annulation |
| `/webhook/` | Endpoint webhook Stripe |
| `/history/` | Historique des paiements |
| `/check-access/` | Vérifier l'accès (API) |

## Modèles de Données

### Product
- `name` - Nom du produit
- `description` - Description
- `price` - Prix en euros
- `stripe_price_id` - ID du prix dans Stripe
- `is_active` - Produit actif ou non

### CheckoutSessionRecord
- `user` - Utilisateur
- `stripe_checkout_session_id` - ID de session Stripe
- `product` - Produit acheté
- `amount_total` - Montant total
- `payment_status` - Statut du paiement
- `is_completed` - Paiement complété
- `has_access` - Accès accordé

### PaymentHistory
- Historique détaillé de tous les paiements

## Commandes Utiles

```bash
# Lancer le serveur
python manage.py runserver

# Créer un superutilisateur
python manage.py createsuperuser

# Accéder à l'administration
# http://127.0.0.1:8000/admin/
```

## Sécurité

- Ne jamais commiter les clés API dans le fichier `.env`
- En production, utilisez `DEBUG = False`
- Configurez `ALLOWED_HOSTS` correctement
- Utilisez HTTPS pour le webhook en production
