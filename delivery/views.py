from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from account.forms import UserForm
from account.models import User, EmailToken
from store.models import Order, OrderStatus, OrderDetail, Product


@login_required(login_url='/account/logining')
def admin_base(request):
    return redirect('orders')


@login_required(login_url='/account/logining')
def orders(request):
    user = request.user
    role = user.roles

    orders = Order.objects.filter(status__id=1)

    context = {
        "list": orders,
        "segment": "del",
    }
    return render(request, 'delivery/orders.html', context=context)


@login_required(login_url='/account/logining')
def getorders(request, id):
    try:
        order = Order.objects.get(id=id)
    except id.DoesNotExist:
        return redirect('myorders')
    status = OrderStatus.objects.get(id=2)
    order.delivery = request.user
    order.status = status
    order.save()
    return redirect('myorders')


@login_required(login_url='/account/logining')
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


@login_required(login_url='/account/logining')
def myorders(request):
    user = request.user
    role = user.roles

    orders = Order.objects.filter(delivery=user).order_by('status')

    context = {
        "list": orders,
        "segment": "myorders",
    }
    return render(request, 'delivery/myorders.html', context=context)


@login_required(login_url='/account/logining')
def orderfinish(request, id):
    user = request.user
    role = user.roles

    order = Order.objects.get(id=id)
    status = OrderStatus.objects.get(id=4)
    order.status = status
    order.save()

    return redirect('myorders')


@login_required(login_url='/account/logining')
def profile(request):
    user = request.user
    role = user.roles

    context = {
        "user": user,
        "segment": "profile",
    }

    return render(request, 'delivery/page-user.html', context=context)


@login_required(login_url='/account/logining')
def admin_deliveries(request):
    users = User.objects.filter(roles__name="DELIVERY")
    return render(request, 'admin/deliveries.html', {'list': users, 'segment': 'delivery'})


def admin_update_deliveries(request, pk):
    if request.method == "GET":
        user = User.objects.get(pk=pk)
        name = user.name
        sname = user.surname
        email = user.email
        phone = user.phone
        icon = user.icon
        return render(request, 'admin/add-delivery.html', {
            'name': name, 'icon': icon, 'sname': sname, 'email_2': email, 'phone': phone, 'segment': 'delivery',
            'action': 'Жаңарту'})

    if request.method == "POST":
        name = request.POST['name']
        surname = request.POST['surname']
        password = request.POST['password']
        phone = request.POST['phone']
        img = request.FILES.get('icon')
        user = User.objects.get(pk=pk)
        user.name = name
        user.surname = surname
        if password:
            user.set_password(password)
        user.phone = phone
        if img:
            user.icon = img
        user.save()

        return redirect('deliveries_list')


@login_required(login_url='/account/logining')
def admin_add_deliveries(request):
    if request.method == "GET":
        return render(request, 'admin/add-delivery.html', {'segment': 'delivery', 'action': "Жеткізетін адамды қосыңыз"})

    if request.method == "POST":
        name = request.POST['name']
        sname = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        img = request.FILES
        context = {
            "name": name,
            "sname": sname,
            "email": email,
            "phone": phone,
            "password": password,
            "message": ""
        }

        user = User.objects.filter(email=email)
        if user.first():
            context["message"] = "Такой email уже существует"
            return render(request, 'admin/add-delivery.html', context=context)

        user = User.objects.filter(phone=phone)
        if user.first():
            context["message"] = "Такой номер уже существует"
            return render(request, 'admin/add-delivery.html', context=context)

        user = User.objects.create(name=name, surname=sname, email=email, phone=phone, icon=img.get('icon'))
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.roles_id = 3
        user.save()
        return redirect("deliveries_list")


def delete_delivery(request, id):
    try:
        del_sel = User.objects.get(pk=id)
    except id.DoesNotExist:
        return redirect('deliveries_list')
    del_sel.delete()
    return redirect('deliveries_list')


def delete_product(request, id):
    try:
        del_sel = Product.objects.get(pk=id)
    except id.DoesNotExist:
        return redirect('admin_products')
    del_sel.delete()
    return redirect('admin_products')
