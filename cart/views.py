from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import CartAddProductForm
from store.models import Product, Order, OrderDetail


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'store/cart.html', {'cart': cart, "count": cart.__len__()})


def checkout(request):
    cart = Cart(request)

    if cart.get_total_price() == 0:
        return redirect('cart:cart_detail')

    if request.method == "POST":
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        phone = request.POST['phone']
        lat = request.POST['lat']
        lng = request.POST['lng']
        #
        # print(lat)
        # print(lng)

        context = {
            "address1": address1,
            "address2": address2,
            "phone": phone,
            'cart': cart,
            "count": cart.__len__()
        }

        if lat == '43.25263391861023' and lng == '76.9166923806056':
            context['error'] = 'Подтвердите адрес из карты'
            return render(request, 'store/checkout.html', context=context)

        order = Order.objects.create(user=request.user, total=cart.get_total_price(),
                                     address1=address1, address2=address2, phone=phone,
                                     lat=lat, lng=lng)

        order.save()

        for item in cart:
            # print(item)
            # order = Order.objects.get(id=order.id)
            product = Product.objects.get(id=item['product'].id)
            order_detail = OrderDetail.objects.create(order=order, product=product,
                                                      price=item['price'], count=item['quantity'],
                                                      total_price=item['total_price'])

            order_detail.save()

        cart = Cart(request)
        cart.clear()

        return redirect('/order')

    return render(request, 'store/checkout.html', {'cart': cart, "count": cart.__len__()})
