from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

# Create your views here.
from account.models import User


def logining(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
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
        sname = request.POST['sname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        img = request.FILES

        context = {
            "name": name,
            "sname": sname,
            "email": email,
            "pass1": pass1,
            "pass2": pass2,
            "message": ""
        }

        user = User.objects.filter(email=email)
        if user.first():
            context["message"] = "Error"
            print("ok")
            return render(request, 'account/register.html', context=context)

        if pass1 != pass2:
            context["message"] = "Error"
            return render(request, 'account/register.html', context=context)

    return render(request, 'account/register.html')
