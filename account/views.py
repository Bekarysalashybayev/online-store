from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Create your views here.
from account.forms import UserForm
from account.models import User, EmailToken


def logining(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(email=username, password=password)
        if user is not None:
            login(request, user)

            return redirect("/account")
        else:
            return render(request, 'account/login.html', context={"message": "Error"})
    # No backend authenticated the credentials

    if not request.user.is_authenticated:
        return render(request, 'account/login.html')
    else:
        return redirect("/account")


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
        else:
            print(user_form.errors)
        auth_user = authenticate(email=email, password=pass1)
        if auth_user is not None:
            login(request, auth_user)

            return redirect("/account")
        else:
            return render(request, 'account/login.html', context={"message": "Error"})
    return render(request, 'account/register.html')


def code(request, pk):
    if request.method == 'POST':
        print(pk)
        user = User.objects.filter(pk=pk).first()
        email_token = EmailToken.objects.filter(email=user.email)

        code = request.POST.get('code')
        print(code)
        print(email_token.first().otp)
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
