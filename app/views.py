from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Banner, Cart, CartItem, Category, InstaPost, Order, Pizza
from django.http import JsonResponse
import collections

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

def menu(request):
    pizzas = Pizza.objects.all()
    categories = Category.objects.all()
    context = {
        'pizzas': pizzas,
        'categories': categories
    }

    return render(request, 'app/menu.html', context)

def details(request, id):
    pizzas = Pizza.objects.all()
    pizza = Pizza.objects.get(id=id)
    context = {'pizza': pizza, 'pizzas': pizzas}

    return render(request, 'app/details.html', context)


def updateItem(request):
    user = request.user

    if request.method == 'POST':
        productId = request.POST['productId']
        action = request.POST['action']

        if request.user.is_anonymous:
            cartItem={}
            cartItem[str(productId)] = {
                'quantity': 1
            }
            if action == 'add':
                if 'cartdata' in request.session:
                    if str(productId) in request.session['cartdata']:
                        cart_data=request.session['cartdata']
                        cart_data[str(productId)]['quantity'] += 1
                        cart_data.update(cart_data)
                        request.session['cartdata']=cart_data
                    else:
                        cart_data=request.session['cartdata']
                        cart_data.update(cartItem)
                        request.session['cartdata']=cart_data
                else:
                    request.session['cartdata']=cartItem     
            elif action == 'remove':
                if 'cartdata' in request.session:
                    if str(productId) in request.session['cartdata']:
                        cart_data=request.session['cartdata']
                        cart_data[str(productId)]['quantity'] -= 1
                        cart_data.update(cart_data)
                        request.session['cartdata']=cart_data
                    
                        if request.session['cartdata'][str(productId)]['quantity'] <= 0:
                            request.session['cartdata'].pop(str(productId))

            elif action == 'delete':
                if 'cartdata' in request.session:
                    request.session['cartdata'].pop(str(productId))
        else:
            pizza = Pizza.objects.get(id=productId)
            cart, created = Cart.objects.get_or_create(user=user)

            cartItem, created = CartItem.objects.get_or_create(cart=cart, product=pizza)

            if action == 'add':
                cartItem.quantity = (cartItem.quantity+1)
                cartItem.save()
            elif action == 'remove':
                cartItem.quantity = (cartItem.quantity-1)
                cartItem.save()
            elif action == 'delete':
                cartItem.delete()


            if cartItem.quantity <= 0:
                cartItem.delete()
    
    if request.user.is_anonymous:
        total = 0

        if 'cartdata' in request.session:
            for key in request.session['cartdata']:
                cart_data=request.session['cartdata']
                total += cart_data[key]['quantity']

        return JsonResponse({'total': total})
    else:
        cart = Cart.objects.get(user=user)
        items = CartItem.objects.filter(cart=cart)
        total = 0
        
        for item in items:
            total = total + item.quantity

        return JsonResponse({'total': total})


def cart(request):
    user = request.user
    if request.user.is_anonymous:
        cart =[]
        if 'cartdata' in request.session:
            for key in request.session['cartdata']:
                cart_data=request.session['cartdata']
                quantity = cart_data[key]['quantity']
                pizza = Pizza.objects.get(id=int(key))
                dictionary = {"quantity":quantity, "product": pizza}
                cartItem = collections.namedtuple("CartItem", dictionary.keys())(*dictionary.values())
                cart.append(cartItem)

        return render(request, 'app/cart.html', {'cart': cart})

    else:
        cart = Cart.objects.get(user=user)
        items = CartItem.objects.filter(cart=cart)

        return render(request, 'app/cart.html', {'cart': items})



def checkout(request):
    user = request.user

    if request.method == 'POST':
        name = request.POST['fname']+' '+request.POST['lname']
        address = request.POST['addr-1'][0]+', '+request.POST['addr-1'][1]+', '+ request.POST['town']
        phone = request.POST['phone']
        email = request.POST['email']
        notes = request.POST['notes']
        total = 0

        if request.user.is_anonymous:
            if 'cartdata' in request.session:
                for key in request.session['cartdata']:
                    cart_data=request.session['cartdata']
                    quantity = cart_data[key]['quantity']
                    pizza = Pizza.objects.get(id=int(key))
                    total += pizza.price * quantity
            
            del request.session['cartdata']
        else:
            cart = Cart.objects.get(user=user)
            items = CartItem.objects.filter(cart=cart)
            for item in items:
                total += item.quantity * item.product.price

            items.delete()
        
        order = Order(name=name, address=address, phone=phone, email=email, notes=notes, amount=total)
        order.save()
        
        return redirect('/')


    if request.user.is_anonymous:
        cart =[]
        if 'cartdata' in request.session:
            for key in request.session['cartdata']:
                cart_data=request.session['cartdata']
                quantity = cart_data[key]['quantity']
                pizza = Pizza.objects.get(id=int(key))
                dictionary = {"quantity":quantity, "product": pizza}
                cartItem = collections.namedtuple("CartItem", dictionary.keys())(*dictionary.values())
                cart.append(cartItem)

        return render(request, 'app/checkout.html', {'cart': cart})

    else:
        cart = Cart.objects.get(user=user)
        items = CartItem.objects.filter(cart=cart)

        return render(request, 'app/checkout.html', {'cart': items})