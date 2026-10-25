from django.contrib import admin
from .models import Book, Order

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'stock')
    search_fields = ('title', 'author', 'isbn')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'created_at')
    list_filter = ('created_at',)