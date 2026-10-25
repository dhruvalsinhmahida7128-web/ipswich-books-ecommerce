# Scope Document — Ipswich Books PoC

**Project:** Proof-of-Concept E-commerce Application for Ipswich Retail
**Author:** DevOps Lead (PoC)
**Version:** 1.1
**Date:** 10/25/2026
**Status:** Approved for build
**Changes from v1.0:** User authentication and profiles added to scope.

---

## 1. Purpose

This document defines the scope of a Proof-of-Concept (PoC) e-commerce web
application for Ipswich Retail, built with Django using a Model-View-Template
(MVT) architecture and delivered under DevOps principles. It exists to
constrain the build to a size that allows full instrumentation of the DevOps
lifecycle (planning → CI → containerization → CD → monitoring) within the PoC
timeframe, while remaining a realistic substitute for the company's existing
monolithic system.

## 2. Product Domain

The PoC is a **book retail storefront**. Books were selected as the domain
because the data model is compact (a single primary catalogue entity), the user
journeys are well understood, and the domain maps cleanly onto the four
required user-facing pages without requiring payment, shipping, or complex
inventory logic.

## 3. In-Scope Pages

### 3.1 Storefront (four core pages)

| # | Page | URL | Purpose |
|---|------|-----|---------|
| 1 | Home / Book List | `/` | Grid of book covers with title, author, price, and "Add to Cart" |
| 2 | Book Detail | `/book/<id>/` | Single-book view: cover, title, author, description, price, quantity selector, "Add to Cart" |
| 3 | Cart | `/cart/` | Session-based cart: line items, quantities, subtotal, "Proceed to Checkout" |
| 4 | Checkout (placeholder) | `/checkout/` | Order summary, form fields, mock "Place Order" — **no real payment processing** |
| — | Django Admin | `/admin/` | CRUD for the Book model; used to load and demonstrate sample data |

### 3.2 Authentication & Account (four supporting views)

| # | Page | URL | Purpose |
|---|------|-----|---------|
| 5 | Register | `/accounts/register/` | `UserCreationForm` — username, email, password |
| 6 | Login | `/accounts/login/` | Built-in `LoginView` |
| 7 | Logout | `/accounts/logout/` | Built-in `LogoutView` (POST-only, CSRF-protected) |
| 8 | Profile | `/accounts/profile/` | Read-only: username, email, join date, order count, recent orders |

> The four core storefront pages satisfy the brief's "±4 pages excluding admin."
> The additional auth and profile pages use Django's built-in `contrib.auth`
> views with **no custom authentication logic**, and exist to support a
> realistic checkout flow rather than as additional feature development.

## 4. Data Model (In Scope)

Three models. `Book` is the catalogue entity; `Order` and `Profile` are
authentication-adjacent models that support the customer journey.

```python
# shop/models.py
class Book(models.Model):
    title       = models.CharField(max_length=200)
    author      = models.CharField(max_length=150)
    isbn        = models.CharField(max_length=13, unique=True)
    description = models.TextField()
    price       = models.DecimalField(max_digits=6, decimal_places=2)
    cover_image = models.ImageField(upload_to='covers/', blank=True)
    stock       = models.PositiveIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE,
                                   null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total      = models.DecimalField(max_digits=8, decimal_places=2)

# accounts/models.py
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
