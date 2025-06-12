from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Product, BlogPost, ContactSubmission, Order

def home(request):
    products = Product.objects.all()  # For now, all products are featured; filter by a 'featured' field if needed later
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html')

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def process(request):
    return render(request, 'process.html')

def aim(request):
    return render(request, 'aim.html')

def blog(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog.html', {'posts': posts})

def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    return render(request, 'blog_detail.html', {'post': post})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if not name or not email or not message:
            messages.error(request, 'Please fill out all fields.')
            return redirect('contact')

        subject = f"New Contact Form Submission from {name}"
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = ['sariakhan7215@gmail.com']

        try:
            send_mail(subject, email_message, from_email, recipient_list, fail_silently=False)
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
        except Exception as e:
            messages.error(request, f'Error sending message: {str(e)}. Please try again later.')

        ContactSubmission.objects.create(name=name, email=email, message=message)
        return redirect('contact')

    return render(request, 'contact.html')

def checkout(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        customer_address = request.POST.get('customer_address')
        city = request.POST.get('city')
        quantity = int(request.POST.get('quantity', 1))
        payment_method = request.POST.get('payment_method')

        if not all([customer_name, customer_email, customer_phone, customer_address, city, payment_method]):
            messages.error(request, 'Please fill out all fields.')
            return render(request, 'checkout.html', {'product': product})

        if payment_method not in ['COD', 'WHATSAPP']:
            messages.error(request, 'Invalid payment method.')
            return render(request, 'checkout.html', {'product': product})

        # Flat shipping fee
        shipping_fee = 199  # Rs 199
        total_amount = (product.price * quantity) + shipping_fee

        # Create order
        order = Order(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            customer_address=customer_address,
            city=city,
            product=product,
            quantity=quantity,
            payment_method=payment_method,
            shipping_fee=shipping_fee,
            total_amount=total_amount
        )
        order.save()

        # Send email to admin
        admin_subject = f"New Order: {order.order_id}"
        admin_message = (
            f"Order ID: {order.order_id}\n"
            f"Customer: {customer_name}\n"
            f"Email: {customer_email}\n"
            f"Phone: {customer_phone}\n"
            f"Address: {customer_address}, {city}\n"
            f"Product: {product.name}\n"
            f"Quantity: {quantity}\n"
            f"Payment Method: {payment_method}\n"
            f"Shipping Fee: Rs {shipping_fee}\n"
            f"Total: Rs {total_amount}"
        )
        try:
            send_mail(
                admin_subject,
                admin_message,
                settings.EMAIL_HOST_USER,
                ['sariakhan7215@gmail.com'],
                fail_silently=False,
            )
        except Exception as e:
            messages.error(request, f'Error sending admin email: {str(e)}.')

        # Send email to customer
        customer_subject = f"Your Agrofer Order Confirmation: {order.order_id}"
        customer_message = (
            f"Thank you for your order, {customer_name}!\n\n"
            f"Order ID: {order.order_id}\n"
            f"Product: {product.name}\n"
            f"Quantity: {quantity}\n"
            f"Payment Method: {payment_method}\n"
            f"Shipping Fee: Rs {shipping_fee}\n"
            f"Total: Rs {total_amount}\n"
            f"Shipping Address: {customer_address}, {city}\n\n"
            f"We’ll notify you once your order is shipped. For COD orders, please prepare Rs {total_amount} for delivery.\n"
            f"Contact us at agrofer.info@gmail.com or +92 310 4358786 for any questions."
        )
        try:
            send_mail(
                customer_subject,
                customer_message,
                settings.EMAIL_HOST_USER,
                [customer_email],
                fail_silently=False,
            )
        except Exception as e:
            messages.error(request, f'Error sending customer email: {str(e)}.')

        if payment_method == 'WHATSAPP':
            whatsapp_url = (
                f"https://wa.me/+923104358786?text=I%20want%20to%20order%20{product.name}%2C%20"
                f"Price%3A%20Rs%20{product.price}%2C%20Quantity%3A%20{quantity}%2C%20"
                f"Shipping%3A%20Rs%20{shipping_fee}%2C%20Total%3A%20Rs%20{total_amount}%2C%20"
                f"Order%20ID%3A%20{order.order_id}"
            )
            return redirect(whatsapp_url)

        messages.success(request, 'Your order has been placed successfully!')
        return redirect('order_confirmation', order_id=order.order_id)

    return render(request, 'checkout.html', {'product': product})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})