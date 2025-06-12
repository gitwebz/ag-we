from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    weight = models.DecimalField(max_digits=10, decimal_places=1)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog/', blank=True, null=True)

    def __str__(self):
        return self.title

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    PAYMENT_METHODS = (
        ('COD', 'Cash on Delivery'),
        ('WHATSAPP', 'WhatsApp Order'),
    )
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=15)
    customer_address = models.TextField()
    city = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=0, default=199)
    total_amount = models.DecimalField(max_digits=10, decimal_places=0)
    order_date = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=20, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"AGRO-{self.id or Order.objects.count() + 1:06d}"
        self.total_amount = (self.product.price * self.quantity) + self.shipping_fee
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id} - {self.customer_name}"