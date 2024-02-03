from django.shortcuts import render


def bl(request):
    return render(request, 'blogs/index.html')