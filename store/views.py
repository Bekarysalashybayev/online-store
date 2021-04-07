from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from cart.cart import Cart
from cart.forms import CartAddProductForm
from store.models import *


@login_required(login_url='account/logining')
def index(request):
    user = request.user
    role = user.roles
    cart = Cart(request)
    products = Product.objects.all()

    return render(request, 'store/index.html', context={"role": role, "list": products, "cart": cart})


def shop(request):
    user = request.user
    role = user.roles

    products = Product.objects.all()

    cart_product_form = CartAddProductForm()
    cart = Cart(request)

    context = {
        "list": products,
        "cart_product_form": cart_product_form,
        "cat": "all",
        "cart": cart,
    }
    return render(request, 'store/categories.html', context=context)


def shopOther(request):
    user = request.user
    role = user.roles

    cart = Cart(request)
    products = Product.objects.filter(category__name="Другое")

    context = {
        "list": products,
        "cat": "other",
        "cart": cart,
    }
    return render(request, 'store/categories.html', context=context)


def shopFeMale(request):
    user = request.user
    role = user.roles
    cart = Cart(request)
    products = Product.objects.filter(category__name="Женский")

    context = {
        "list": products,
        "cat": "female",
        "cart": cart,
    }
    return render(request, 'store/categories.html', context=context)


def shopMale(request):
    user = request.user
    role = user.roles
    cart = Cart(request)
    products = Product.objects.filter(category__name="Мужской")

    context = {
        "list": products,
        "cat": "muj",
        "cart": cart,
    }
    return render(request, 'store/categories.html', context=context)


def product(request, id):
    user = request.user
    role = user.roles

    product = Product.objects.get(id=id)
    list = Product.objects.filter(category=product.category)
    cart_product_form = CartAddProductForm()
    cart = Cart(request)

    context = {
        "product": product,
        "list": list,
        "cart_product_form": cart_product_form,
        "cat": "all",
        "cart": cart,
    }
    return render(request, 'store/product.html', context=context)


def blog(request):
    user = request.user
    role = user.roles
    cart = Cart(request)
    context = {
        'cart': cart
    }
    return render(request, 'store/blog.html', context=context)


def orders(request):
    user = request.user
    role = user.roles

    cart = Cart(request)
    order = Order.objects.filter(user=user).order_by('-pk')
    context = {
        'order': order,
        'cart': cart
    }
    return render(request, 'store/Orders.html', context=context)


def detail(request, id):
    user = request.user
    role = user.roles
    cart = Cart(request)
    order = Order.objects.get(id=id)
    detail = OrderDetail.objects.filter(order=order)
    context = {
        'order': order,
        'detail': detail,
        'cart': cart
    }
    return render(request, 'store/orderdetail.html', context=context)
