from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import datetime

from .models import *
from .forms import OrderForm, CreateUserForm
from .decorators import unauthenticated_user, allowed_users, admin_only
from .utils import cartData


# Create your views here.
@unauthenticated_user
def registerpage(request):
    form = CreateUserForm()  # it creates by default user registration fields

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')  # to get username not other thing

            group = Group.objects.get(name='costumer')  # user gets automatically costumer when register
            user.groups.add(group)  # creates a group on registration
            Costumer.objects.create(
                user=user,
                name=user.username,
            )

            messages.success(request, 'Account was created for' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'username or pass is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutpage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
# you are not able to see these kinds of pages without being login
def dashboard(request):
    orders = Order.objects.all()
    costumers = Costumer.objects.all()

    total_costumers = costumers.count()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders,
               'costumers': costumers,
               'total_costumers': total_costumers,
               'total_orders': total_orders,
               'delivered': delivered,
               'pending': pending
               }

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['costumer'])
def userpage(request):
    orders = request.user.costumer.order_set.all()  # query that takes all orders from costumer

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders,
               'total_orders': total_orders,
               'delivered': delivered,
               'pending': pending
               }
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def costumer(request, pk):
    # primarykey = pk
    costumer = Costumer.objects.get(id=pk)

    order = costumer.order_set.all()
    order_count = order.count()

    context = {'costumer': costumer,
               'order': order,
               'order_count': order_count
               }

    return render(request, 'accounts/costumer.html', context)


def deletecostumer(request, pk):
    costumer = Costumer.objects.get(id=pk)
    if request.method == "POST":  # admin request to delete it
        costumer.delete()
        return redirect('/')
    context = {'costumer': costumer}

    return render(request, 'accounts/deleteCostumer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createorder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('/')  # send back to the main template

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateorder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)  # in this case we see pre filled with costumer info

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteorder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/deleteOrder.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['costumer'])
def newproducts(request):
    new_products = Product.objects.all()
    context = {'new_products': new_products}
    return render(request, 'accounts/new_products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['costumer'])
def home(request):
    home = Product.objects.all()
    context = {'home': home}
    return render(request, 'accounts/home.html', context)


def aboutus(request):
    home = Product.objects.all()
    context = {'home': home}
    return render(request, 'accounts/aboutus.html', context)


def productDetails(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'accounts/product_details.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['costumer'])
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'accounts/store.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['costumer'])
def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'accounts/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'accounts/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    costumer = request.user.costumer
    product = Product.objects.get(id=productId)

    order = Order.objects.filter(costumer=costumer, complete=False)
    if not order.exists():
        order = Order.objects.create(costumer=costumer, complete=False)
    else:
        order = order.last()

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)








