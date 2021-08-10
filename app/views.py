from django.shortcuts import render
from .models import Banner, InstaPost, Pizza

# Create your views here.

def home(request):
    insta_posts = InstaPost.objects.all()
    banners = Banner.objects.all()
    pizzas = Pizza.objects.all()
    context = {
        'insta_posts': insta_posts,
        'banners': banners,
        'pizzas': pizzas
    }
    return render(request, 'app/home.html', context)

def privacy(request):
    return render(request, 'app/privacy-policy.html')

def cookie(request):
    return render(request, 'app/cookie-policy.html')

def terms(request):
    return render(request, 'app/terms.html')

def refund(request):
    return render(request, 'app/refund-policy.html')

def error_404_view(request, exception):
    context = {'exceptions': exception}
    return render(request, 'app/404.html', context)