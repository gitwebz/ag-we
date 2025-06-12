from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('process/', views.process, name='process'),
    path('aim/', views.aim, name='aim'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:post_id>/', views.blog_detail, name='blog_detail'),
    path('contact/', views.contact, name='contact'),
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('order-confirmation/<str:order_id>/', views.order_confirmation, name='order_confirmation'),
]