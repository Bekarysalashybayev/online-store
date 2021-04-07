from django.shortcuts import render


# Create your views here.
def admin_base(request):
    user = request.user
    role = user.roles
    return render(request, 'delivery/index.html')
