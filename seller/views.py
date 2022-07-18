from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib import messages
import mysql.connector as sql
from seller.models import Seller, Product
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.models import User

# Create your views here.

class LoginSeller(View):
    def get(self, request):
        return render(request, "slogin.html")

    def post(self, request):
        if request.method=="POST":
            username=request.POST['username']
            password=request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('seller_product')
            else:
                messages.error(request, "Invalid credentials")
                return redirect('seller_login')

                #obj = Seller.objects.get(email=email)       
                #if password == obj.password:
                    #request.session['member_id'] = obj.id
                    #return redirect('product')
                #else:
                    #messages.error(request, "Invalid password")
                    #return redirect('seller_login')
            
        return render(request, "slogin.html")


def logout_user(request):
    request.session.clear()
    return redirect('logout')
     
class SignupSeller(View):
    def get(self, request):
        return render(request,"ssignup.html")

    def post(self, request):
        if request.method == 'POST':
            username=request.POST['username']
            fname=request.POST['fname']
            comp_name=request.POST['comp_name']
            email=request.POST['email']
            password=request.POST['password']
            try:
                obj=User.objects.create_user(username=username, email=email, first_name=fname, password=password) 
                obj.save()
                cust=Seller(user_id=obj.id, email=email, fname=fname, comp_name=comp_name, password=password)
                cust.save()

                messages.success(request, "Account created successfully!")
                return redirect('seller_login')

            except IntegrityError:
                messages.warning(request, "Account already exists")
                #messages.error(request, "Registration Unsuccessful!")
                return render(request,"seller_signup.html")        
        return render(request,"seller_signup.html") 

def add_product(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            prodname=request.POST['prodname']
            price=request.POST['price']
            desc=request.POST['desc']
            prodimg=request.FILES['prodimg']
            cust=Seller.objects.get(user=request.user)
            obj=Product.objects.create(prodname=prodname, price=price,desc=desc, prodimg=prodimg, shop=cust)
            obj.save()
            messages.success(request,"Product added successfully")
        return render(request, "add_product.html")

    return render(request, "add_product.html")


def viewProduct(request):
    if request.user.is_authenticated:
        order=Seller.objects.get(user=request.user)
        print(order)
        products=Product.objects.filter(shop=order)
        context={'products': products}
    return render(request, "products.html", context)