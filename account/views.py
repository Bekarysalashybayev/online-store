from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from account.forms import UserForm
from account.models import User, EmailToken


def logining(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(email=username, password=password)
        if user is not None:
            login(request, user)
            role = user.roles
            if role.name == 'USER':
                return redirect('store_index')
            if role.name == 'ADMIN':
                return redirect('admin_products')
            if role.name == 'DELIVERY':
                return redirect('orders')
            return redirect("/")
        else:
            return render(request, 'account/login.html', context={"message": "Error"})

    if not request.user.is_authenticated:
        return render(request, 'account/login.html')
    else:
        role = request.user.roles
        if role.name == 'USER':
            return redirect('store_index')
        if role.name == 'ADMIN':
            return redirect('admin_products')
        if role.name == 'DELIVERY':
            return redirect('orders')
            return redirect("/")


def logout_view(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == "POST":
        name = request.POST['name']
        sname = request.POST['surname']
        email = request.POST['email']
        pass1 = request.POST['password1']
        phone = request.POST['phone']
        pass2 = request.POST['password2']
        img = request.FILES
        context = {
            "name": name,
            "sname": sname,
            "email": email,
            "phone": phone,
            "pass1": pass1,
            "pass2": pass2,
            "message": ""
        }
        if not img.get('icon'):
            context["message"] = "Выберите фото"
            return render(request, 'account/register.html', context=context)

        user = User.objects.filter(email=email)
        if user.first():
            context["message"] = "Такой email уже существует"
            return render(request, 'account/register.html', context=context)
        user = User.objects.filter(phone=phone)

        if user.first():
            context["message"] = "Такой номер уже существует"
            return render(request, 'account/register.html', context=context)

        if pass1 != pass2:
            context["message"] = "пароли не совпадают"
            return render(request, 'account/register.html', context=context)
        user_form = UserForm(request.POST, request.FILES)
        if user_form.is_valid():
            instance = user_form.save(commit=False)
            instance.save()
            otp = EmailToken.create_otp_for_number(email)
            return redirect('code', pk=instance.pk)

            return redirect("/account")
        else:
            return render(request, 'account/login.html', context={"message": "Error"})
    return render(request, 'account/register.html')


def code(request, pk):
    if request.method == 'POST':
        user = User.objects.filter(pk=pk).first()
        email_token = EmailToken.objects.filter(email=user.email)
        code = request.POST.get('code')
        if int(email_token.first().otp) == int(code):
            user.is_active = True
            user.is_staff = True
            user.save()
            email_token = email_token.first()
            email_token.used = True
            email_token.attempts += 1
            email_token.save()

            return redirect("/account/logining")

    return render(request, 'account/code.html', {'pk': pk})
