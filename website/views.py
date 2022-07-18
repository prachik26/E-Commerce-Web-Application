from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib import messages
import mysql.connector as sql
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from requests import request
from website.models import Customer,Order,OrderItem,ShippingAddress
from seller.models import Product
from django.views import View
from django.contrib.auth.decorators import login_required
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
import razorpay

def home(request):
    return render(request, "base.html")

class LoginUser(View):
    def get(self, request):
        return render(request, "clogin.html")

    def post(self, request):
        if request.method=="POST":
            m=sql.connect(host="localhost", user="root", passwd="prachi26", database='shopping')
            username=request.POST['username']
            email=request.POST['email']
            password=request.POST['password']
            obj=authenticate(request, username=username, password=password, email=email)
            if obj is not None:
                login(request, obj)
                return redirect('store')
            else:
                messages.error(request, "Invalid password")
                return redirect('login')

            # try:
            #     obj = Customer.objects.get(username=username,email=email)       
            #     if password == obj.password:
            #         request.session['member_id'] = obj.id
            #         print(request.session['member_id'])
            #         return redirect('store')
                
            #     else:
            #         messages.error(request, "Invalid password")
            #         return redirect('login')
           
            # except Customer.DoesNotExist:
            #     messages.error(request, "Email does not exist")
            #     return redirect('login')
            
        return render(request, "clogin.html")


def logout_user(request):
    if request.method=='GET':
       request.session.clear()
    return render(request,'logout.html')
     
class Signup(View):
    def get(self, request):
        return render(request,"csignup.html")

    def post(self, request):
        if request.method == 'POST':
            m=sql.connect(host="localhost", user="root", passwd="prachi26", database='shopping')
            username=request.POST['username']
            fname=request.POST['fname']
            email=request.POST['email']
            password=request.POST['password']
            try:
                obj= User.objects.create_user(username, email, password)
                obj.save()
                cust=Customer.objects.create(user_id=obj.id,fname=fname,email=email,password=password) 
                cust.save()
                m.commit()
                messages.success(request, "Account created successfully!")
                return redirect('login') 
            except IntegrityError:
                messages.warning(request, "Account already exists")
                return redirect('signup')
                     
        return render(request,"csignup.html") 

def welcome(request):
    if request.user.is_authenticated:        
        customer=Customer.objects.get(user=request.user)
        print(customer)
        order, created=Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems=order.get_cart_items
    
    products=Product.objects.all()
    context={'products': products, 'cartItems': cartItems}
    return render(request, "store.html", context)

@login_required(login_url='/login/')
def cart(request):
    if request.user.is_authenticated:        
        customer=Customer.objects.get(user=request.user)
        order, created=Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems=order.get_cart_items
    
    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, "cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer=Customer.objects.get(user=request.user)
        order, created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    
    context = {'items':items, 'order':order, 'cartItems': cartItems}
    return render(request, "checkout.html",context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    customer=Customer.objects.get(user=request.user)
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    
    if total == order.get_cart_total:
        order.complete = True
    order.save()
    
    if order.shipping == True:
        ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
        phone=data['shipping']['phone'],
		)
    
    client=razorpay.Client(auth=('rzp_test_PYOtJ86UENY04m', 'dqQpDhNiYtK6NqoK27hqVPZX'))
    payment=razorpay.order.create({'amount':50000, 'currency':'INR', 'payment_capture':1})
    return render(request, "success.html")

def success():
    if request.method=="POST":
        return render(request, "success.html")
    return render(request, "success.html")