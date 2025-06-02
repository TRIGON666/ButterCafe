from django.db import models
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='categories/', blank=True, verbose_name='Изображение')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name='Цена')
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    available = models.BooleanField(default=True, verbose_name='Доступен')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    calories = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name='Калорийность (ккал)')
    proteins = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name='Белки (г)')
    fats = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name='Жиры (г)')
    carbs = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, verbose_name='Углеводы (г)')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return self.name

class Cart(models.Model):
    session_key = models.CharField(max_length=40, unique=True, verbose_name='Ключ сессии')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина {self.session_key}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='Количество')

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'
        unique_together = ('cart', 'product')

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    @property
    def total_price(self):
        return self.quantity * self.product.price

class Order(models.Model):
    DELIVERY_CHOICES = [
        ('pickup_10a', 'Самовывоз с Лобачевского 10а'),
        ('pickup_43', 'Самовывоз с Щапова 43'),
        ('pickup_51', 'Самовывоз с Сибгата Хакима 51 (ЖК Столичный)'),
        ('pickup_20a', 'Самовывоз с Чистопольской 20а'),
        ('delivery', 'Доставка'),
    ]
    name = models.CharField(max_length=100, verbose_name='Имя')
    phone = models.CharField(max_length=30, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Email')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')
    delivery_type = models.CharField(max_length=32, choices=DELIVERY_CHOICES, verbose_name='Способ получения')
    need_cutlery = models.BooleanField(default=True, verbose_name='Одноразовые приборы')
    need_call = models.BooleanField(default=True, verbose_name='Звонок для подтверждения')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    time = models.CharField(max_length=20, blank=True, verbose_name='Время к заказу')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма заказа')
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Стоимость доставки')
    items_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Стоимость товаров')
    receipt_text = models.TextField(blank=True, verbose_name='Чек (текст)')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']

    def __str__(self):
        return f'Заказ #{self.id} от {self.name}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'
