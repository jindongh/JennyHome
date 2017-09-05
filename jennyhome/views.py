from django.shortcuts import render

def home(request):
    context = {}
    return render(request, 'jennyhome/home.html', context)

