from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def get_cart(request):
    if not request.session.session_key:
        request.session.create()
    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

def get_cart_items_count(request):
    cart = get_cart(request)
    return sum(item.quantity for item in cart.items.all())

def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(available=True)[:6]
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'cart_items_count': get_cart_items_count(request)
    }
    return render(request, 'home.html', context)

def menu(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    category_id = request.GET.get('category')
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'categories': categories,
        'products': products,
        'cart_items_count': get_cart_items_count(request)
    }
    return render(request, 'menu.html', context)

def cart(request):
    cart = get_cart(request)
    cart_items = cart.items.all()
    total_price = sum(item.total_price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_items_count': sum(item.quantity for item in cart_items)
    }
    return render(request, 'cart.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    cart = get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_items_count': sum(item.quantity for item in cart.items.all())})
    messages.success(request, f'Товар "{product.name}" добавлен в корзину')
    return redirect('cart')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart=get_cart(request))
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'Товар "{product_name}" удален из корзины')
    return redirect('cafe:cart')

def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart=get_cart(request))
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cafe:cart')

def product_modal(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    html = render_to_string('product_modal.html', {'product': product, 'cart_items_count': get_cart_items_count(request)}, request=request)
    return JsonResponse({'html': html})

def order_modal(request):
    cart = get_cart(request)
    cart_items = cart.items.all()
    items_price = sum(item.total_price for item in cart_items)
    delivery_price = 100 if cart_items else 0
    total = items_price + delivery_price
    html = render_to_string('order_modal.html', {
        'cart_items': cart_items,
        'items_price': items_price,
        'delivery_price': delivery_price,
        'total': total
    }, request=request)
    return JsonResponse({'html': html})

@require_POST
def order_create(request):
    cart = get_cart(request)
    cart_items = cart.items.all()
    items_price = sum(item.total_price for item in cart_items)
    delivery_price = 100 if cart_items else 0
    total = items_price + delivery_price
    data = request.POST
    try:
        # Формируем текст чека
        receipt_lines = [
            f'Заказ от: {data.get("name", "")}\nТелефон: {data.get("phone", "")}\nEmail: {data.get("email", "")}\n',
            f'Способ получения: {dict(Order.DELIVERY_CHOICES).get(data.get("delivery_type", ""), "")}\n',
            f'Адрес: {data.get("address", "")}\n',
            'Состав заказа:'
        ]
        for item in cart_items:
            receipt_lines.append(f'- {item.product.name} × {item.quantity} = {item.total_price} р.')
        receipt_lines += [
            f'\nСтоимость товаров: {items_price} р.',
            f'Доставка: {delivery_price} р.',
            f'Итого: {total} р.',
            f'Комментарий: {data.get("comment", "")}\n',
            f'Время к заказу: {data.get("time", "")}\n',
            f'Одноразовые приборы: {"Да" if data.get("need_cutlery") else "Нет"}',
            f'Звонок для подтверждения: {"Да" if data.get("need_call") else "Нет"}',
        ]
        receipt_text = '\n'.join(receipt_lines)
        order = Order.objects.create(
            name=data.get('name', ''),
            phone=data.get('phone', ''),
            email=data.get('email', ''),
            address=data.get('address', ''),
            delivery_type=data.get('delivery_type', ''),
            need_cutlery=bool(data.get('need_cutlery')),
            need_call=bool(data.get('need_call')),
            comment=data.get('comment', ''),
            time=data.get('time', ''),
            total=total,
            delivery_price=delivery_price,
            items_price=items_price,
            receipt_text=receipt_text
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart.items.all().delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'errors': [str(e)]})

def about(request):
    context = {
        'cart_items_count': get_cart_items_count(request)
    }
    return render(request, 'about.html', context)
