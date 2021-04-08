from django.shortcuts import render, redirect

# Create your views here.
from account.models import User
from store.models import Order, OrderStatus, OrderDetail


def admin_base(request):
    return redirect('orders')


# Create your views here.
def orders(request):
    user = request.user
    role = user.roles

    orders = Order.objects.filter(status__id=1)

    context = {
        "list": orders,
        "segment": "del",
    }
    return render(request, 'delivery/orders.html', context=context)


def getorders(request, id):
    user = request.user
    role = user.roles

    order = Order.objects.get(id=id)
    status = OrderStatus.objects.get(id=2)
    order.delivery = user
    order.status = status
    order.save()

    return redirect('myorders')


def deliveryorders(request, id):
    user = request.user
    role = user.roles

    order = Order.objects.get(id=id)

    if order.status.id != 3:
        status = OrderStatus.objects.get(id=3)
        order.status = status
        order.save()

    detail = OrderDetail.objects.filter(order=order)

    context = {
        "order": order,
        "list": detail,
        "segment": "myorders",
    }
    return render(request, 'delivery/myordersdetail.html', context=context)


# Create your views here.
def myorders(request):
    user = request.user
    role = user.roles

    orders = Order.objects.filter(delivery=user).order_by('status')

    context = {
        "list": orders,
        "segment": "myorders",
    }
    return render(request, 'delivery/myorders.html', context=context)


def orderfinish(request, id):
    user = request.user
    role = user.roles

    order = Order.objects.get(id=id)
    status = OrderStatus.objects.get(id=4)
    order.status = status
    order.save()

    return redirect('myorders')


# Create your views here.
def profile(request):
    user = request.user
    role = user.roles

    context = {
        "user": user,
        "segment": "profile",
    }

    return render(request, 'delivery/page-user.html', context=context)




def admin_deliveries(request):
    users = User.objects.filter(roles__name="DELIVERY")
    return render(request, 'admin/deliveries.html', {'list': users, 'segment': 'delivery'})


def admin_add_deliveries(request):
    if request.method == "GET":
        return render(request, 'admin/add-delivery.html', {'segment': 'delivery'})