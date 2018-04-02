from django.shortcuts import render


def home(request):
    if request.user.is_authenticated is False:
        return render(request , 'launchApp/home.html')
    else:
        return render(request , 'launchApp/workspace.html')
