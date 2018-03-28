from django.shortcuts import render


def home(request):
    if request.user.is_authenticated is False:
        return render(request , 'authentification/home.html')
    else:
        return render(request , 'authentification/workspace.html')
