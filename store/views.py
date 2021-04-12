from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from cart.cart import Cart
from cart.forms import CartAddProductForm
from store.models import *


@login_required(login_url='/account/logining')
def index(request):
    user = request.user
    role = user.roles
    cart = Cart(request)
    products = Product.objects.all()
    blog = Blog.objects.all()[:2]

    return render(request, 'store/index.html', context={"role": role, "list": products, "cart": cart, "count":  cart.__len__(), "blog": blog})


@login_required(login_url='/account/logining')
def shop(request):
    user = request.user
    role = user.roles

    products = Product.objects.all()

    cart_product_form = CartAddProductForm()
    cart = Cart(request)

    blog = Blog.objects.all()[:2]

    context = {
        "list": products,
        "cart_product_form": cart_product_form,
        "cat": "all",
        "cart": cart,
        "count": cart.__len__(),
        "blog": blog,
    }
    return render(request, 'store/categories.html', context=context)


@login_required(login_url='/account/logining')
def shopOther(request):
    user = request.user
    role = user.roles

    cart = Cart(request)
    products = Product.objects.filter(category__name="Другое")
    blog = Blog.objects.all()[:2]

    context = {
        "list": products,
        "cat": "other",
        "cart": cart,
        "count": cart.__len__(),
        "blog": blog,
    }
    return render(request, 'store/categories.html', context=context)


@login_required(login_url='/account/logining')
def shopFeMale(request):
    user = request.user
    role = user.roles
    cart = Cart(request)
    products = Product.objects.filter(category__name="Женский")
    blog = Blog.objects.all()[:2]

    context = {
        "list": products,
        "cat": "female",
        "cart": cart,
        "count": cart.__len__(),
        "blog": blog,
    }
    return render(request, 'store/categories.html', context=context)


@login_required(login_url='/account/logining')
def shopMale(request):
    user = request.user
    role = user.roles
    cart = Cart(request)
    products = Product.objects.filter(category__name="Мужской")
    blog = Blog.objects.all()[:2]

    context = {
        "list": products,
        "cat": "muj",
        "cart": cart,
        "count": cart.__len__(),
        "blog": blog,
    }
    return render(request, 'store/categories.html', context=context)


@login_required(login_url='/account/logining')
def product(request, id):
    user = request.user
    role = user.roles

    product = Product.objects.get(id=id)
    list = Product.objects.filter(category=product.category)
    cart_product_form = CartAddProductForm()
    cart = Cart(request)
    blog = Blog.objects.all()[:2]

    context = {
        "product": product,
        "list": list,
        "cart_product_form": cart_product_form,
        "cat": "all",
        "cart": cart,
        "count": cart.__len__(),
        "blog": blog,
    }
    return render(request, 'store/product.html', context=context)


@login_required(login_url='/account/logining')
def blog(request):
    user = request.user
    role = user.roles
    cart = Cart(request)
    blog = Blog.objects.all()

    context = {
        'cart': cart,
        "count": cart.__len__(),
        "blogs": blog,
        "blog": blog[:2],
    }
    return render(request, 'store/blog.html', context=context)


@login_required(login_url='/account/logining')
def orders(request):
    user = request.user
    role = user.roles

    cart = Cart(request)
    order = Order.objects.filter(user=user).order_by('-pk')
    blog = Blog.objects.all()[:2]

    context = {
        'order': order,
        'cart': cart,
        "count": cart.__len__(),
        "blog": blog,
    }
    return render(request, 'store/Orders.html', context=context)


@login_required(login_url='/account/logining')
def detail(request, id):
    user = request.user
    role = user.roles
    cart = Cart(request)
    order = Order.objects.get(id=id)
    detail = OrderDetail.objects.filter(order=order)
    blog = Blog.objects.all()[:2]

    context = {
        'order': order,
        'detail': detail,
        'cart': cart,
        "count": cart.__len__(),
        "blog": blog,
    }
    return render(request, 'store/orderdetail.html', context=context)


@login_required(login_url='/account/logining')
def admin_add_product(request):
    if request.method == "POST":
        data = request.POST
        name = data.get('name')
        price = data.get('price')
        description = data.get('description')
        category = data.get('category')
        status = data.get('status')
        files = request.FILES
        img1 = files.get('img1')
        img2 = files.get('img2')
        img3 = files.get('img3')
        img4 = files.get('img4')
        img5 = files.get('img5')
        product = Product.objects.create(
            name=name, price=price, description=description, category_id=category, status_id=status,
            img1=img1, img2=img2, img3=img3, img4=img4, img5=img5
        )

        return render(request, 'admin/add-product.html', {"segment": "products"})

    if request.method == "GET":
        categories = Category.objects.all()
        statuses = Status.objects.all()
        context = {
            'categories': categories,
            'statuses': statuses,
            "segment": "products",
            'action': 'Добавить продукт'
        }
        return render(request, 'admin/add-product.html', context)


@login_required(login_url='/account/logining')
def admin_products(request):
    list = Product.objects.all().order_by('-pk')
    return render(request, 'admin/products.html', {'list': list, "segment": "products"})


def update_product(request, pk):
    if request.method == "GET":
        categories = Category.objects.all()
        statuses = Status.objects.all()
        product = Product.objects.get(pk=pk)
        return render(request, 'admin/add-product.html', {"segment": "products", 'product': product, 'categories': categories,
            'statuses': statuses, 'action': 'Обновить продукт'})

    if request.method == "POST":
        if request.method == "POST":
            data = request.POST
            name = data.get('name')
            price = data.get('price')
            description = data.get('description')
            category = data.get('category')
            status = data.get('status')
            files = request.FILES
            img1 = files.get('img1')
            img2 = files.get('img2')
            img3 = files.get('img3')
            img4 = files.get('img4')
            img5 = files.get('img5')

            product = Product.objects.get(pk=pk)
            product.name = name
            product.price = price
            product.description = description
            product.category_id = category
            product.status_id = status
            if img5:product.img5 = img5
            if img4:product.img4 = img4
            if img3:product.img3 = img3
            if img2:product.img2 = img2
            if img1:product.img1 = img1
            product.save()

            return redirect('admin_products')

def admin_blog_list(request):
    list = Blog.objects.all().order_by('-pk')
    return render(request, 'admin/blogs.html', {'list': list, "segment": "blog"})


def add_blog_admin(request):
    if request.method == "GET":
        return render(request, 'admin/add-blog.html', {"segment": "blog", 'action': 'Добавить'})

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        img = request.FILES.get('img')

        blog = Blog.objects.create(name=name, img=img, description=description)

        return redirect('admin_blog_list')


def update_blog_admin(request, pk):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        img = request.FILES.get('img')
        print(img)
        blog = Blog.objects.get(pk=pk)
        blog.name = name
        blog.description = description
        if img:
            blog.img = img
        blog.save()

        return redirect('admin_blog_list')

    if request.method == "GET":
        blog = Blog.objects.get(pk=pk)
        name = blog.name
        description = blog.description
        img = blog.img
        return render(request, 'admin/add-blog.html', {'name': name, 'description': description, 'img': img,
                                                       'segment': 'blog', 'action': 'Обновить'})


def delete_blog_admin(request, pk):
    try:
        del_sel = Blog.objects.get(pk=pk)
    except id.DoesNotExist:
        return redirect('admin_blog_list')
    del_sel.delete()
    return redirect('admin_blog_list')


def order_list_admin(request):
    list = Order.objects.all()
    return render(request, 'admin/Orders.html', {'list': list, "segment": "order"})


def order_detail_list_admin(request, pk):
    order = Order.objects.get(pk=pk)
    list = OrderDetail.objects.filter(order=order)
    return render(request, 'admin/order-details.html', {'order': order, 'list': list, "segment": "order"})
