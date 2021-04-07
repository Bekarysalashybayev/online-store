from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from cart.forms import CartAddProductForm
from store.models import *


@login_required(login_url='account/logining')
def index(request):
    user = request.user
    role = user.roles

    return render(request, 'store/index.html', context={"role": role})


def shop(request):
    user = request.user
    role = user.roles

    products = Product.objects.all()

    cart_product_form = CartAddProductForm()

    context = {
        "list": products,
        "cart_product_form": cart_product_form,
        "cat": "all",
    }
    return render(request, 'store/categories.html', context=context)


def shopOther(request):
    user = request.user
    role = user.roles

    products = Product.objects.filter(category__name="Другое")

    context = {
        "list": products,
        "cat": "other",
    }
    return render(request, 'store/categories.html', context=context)


def shopFeMale(request):
    user = request.user
    role = user.roles

    products = Product.objects.filter(category__name="Женский")

    context = {
        "list": products,
        "cat": "female",
    }
    return render(request, 'store/categories.html', context=context)


def shopMale(request):
    user = request.user
    role = user.roles

    products = Product.objects.filter(category__name="Мужской")

    context = {
        "list": products,
        "cat": "muj",
    }
    return render(request, 'store/categories.html', context=context)


def blog(request):
    user = request.user
    role = user.roles

    return render(request, 'store/blog.html')


def orders(request):
    user = request.user
    role = user.roles

    order = Order.objects.filter(user=user).order_by('-pk')
    context = {
        'order': order
    }
    return render(request, 'store/Orders.html', context=context)


def detail(request, id):
    user = request.user
    role = user.roles

    order = Order.objects.get(id=id)
    detail = OrderDetail.objects.filter(order=order)
    context = {
        'order': order,
        'detail': detail
    }
    return render(request, 'store/orderdetail.html', context=context)



