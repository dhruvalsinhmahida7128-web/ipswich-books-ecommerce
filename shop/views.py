from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Order


def home(request):
    books = Book.objects.all()
    return render(request, 'shop/book_list.html', {'books': books})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'shop/book_detail.html', {'book': book})


def cart(request):
    # Session-based cart (simple dictionary of book_id -> quantity)
    cart_data = request.session.get('cart', {})
    cart_items = []
    total = 0
    for book_id, quantity in cart_data.items():
        book = get_object_or_404(Book, pk=book_id)
        subtotal = book.price * quantity
        total += subtotal
        cart_items.append({'book': book, 'quantity': quantity, 'subtotal': subtotal})

    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})


def add_to_cart(request, pk):
    book = get_object_or_404(Book, pk=pk)
    cart_data = request.session.get('cart', {})
    cart_data[str(pk)] = cart_data.get(str(pk), 0) + 1
    request.session['cart'] = cart_data
    return redirect('cart')


def checkout(request):
    cart_data = request.session.get('cart', {})
    if not cart_data:
        return redirect('home')

    total = 0
    for book_id, quantity in cart_data.items():
        book = get_object_or_404(Book, pk=book_id)
        total += book.price * quantity

    # Create the order record
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        total=total
    )

    # Clear the cart
    request.session['cart'] = {}

    return render(request, 'shop/checkout_success.html', {'order': order})