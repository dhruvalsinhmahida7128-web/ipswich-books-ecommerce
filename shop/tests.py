from django.test import TestCase, Client
from django.urls import reverse
from .models import Book, Order
from django.contrib.auth.models import User


class StorefrontTests(TestCase):
    def setUp(self):
        # This runs before every test method
        self.client = Client()
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            description="A test book",
            price=10.00,
            stock=5
        )

    def test_home_page_status_code(self):
        """Test that the home page loads successfully."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")

    def test_book_detail_view(self):
        """Test that the book detail page shows the correct book."""
        response = self.client.get(reverse('book_detail', args=[self.book.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")
        self.assertContains(response, "£10.00")

    def test_add_to_cart(self):
        """Test that adding a book to the cart updates the session."""
        response = self.client.get(reverse('add_to_cart', args=[self.book.pk]))
        # Should redirect to the cart page
        self.assertRedirects(response, reverse('cart'))

        # Check the session data
        session = self.client.session
        self.assertEqual(session['cart'][str(self.book.pk)], 1)

    def test_cart_view(self):
        """Test the cart displays items and totals correctly."""
        # Add 2 books to the cart
        session = self.client.session
        session['cart'] = {str(self.book.pk): 2}
        session.save()

        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")
        self.assertContains(response, "£20.00")  # 2 * 10.00

    def test_checkout_creates_order(self):
        """Test that checkout creates an Order record and clears the cart."""
        # Setup cart
        session = self.client.session
        session['cart'] = {str(self.book.pk): 1}
        session.save()

        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)

        # Check that an order was created
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.total, 10.00)

        # Check that the cart was emptied
        session = self.client.session
        self.assertEqual(session['cart'], {})