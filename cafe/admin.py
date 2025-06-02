from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'available', 'calories', 'proteins', 'fats', 'carbs', 'created', 'updated')
    list_filter = ('available', 'created', 'updated', 'category')
    list_editable = ('price', 'available')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    date_hierarchy = 'created'

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'created', 'updated')
    inlines = [CartItemInline]
    readonly_fields = ('created', 'updated')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'delivery_type', 'total', 'created', 'receipt_text')
    list_filter = ('delivery_type', 'created')
    search_fields = ('name', 'phone', 'email', 'address')
    readonly_fields = ('created', 'total', 'delivery_price', 'items_price', 'receipt_text')
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('name', 'phone', 'email', 'delivery_type', 'address', 'created', 'total', 'delivery_price', 'items_price')
        }),
        ('Детали заказа', {
            'fields': ('need_cutlery', 'need_call', 'comment', 'time')
        }),
        ('Чек', {
            'fields': ('receipt_text',)
        })
    )
