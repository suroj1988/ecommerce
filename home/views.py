import datetime

from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib import sessions

# Create your views here.
class Base(View):
    views = {}
    views['categories'] = Category.objects.all()

class Home(Base):
    def get(self,request):
        self.views
        self.views['sliders'] = Slider.objects.all()
        self.views['ads'] = Ad.objects.all()
        self.views['hots'] = Product.objects.filter(label='hot')
        self.views['news'] = Product.objects.filter(label='new')
        self.views['sales'] = Product.objects.filter(label='sale')
        return render(request,'index.html',self.views)
class Cat(Base):
    def get(self,request,slug):
        self.views
        ids = Category.objects.get(slug=slug).id
        self.views['catproduct'] = Product.objects.filter(category_id=ids)
        return render(request,'category.html',self.views)
class Search(Base):
    def get(self,request):

        if request.method == 'GET':

            query = request.GET['query']
            if query == '':
                return redirect('/')
            else:
                 self.views['searchproduct'] = Product.objects.filter(name__icontains = query)

        return render(request,'search.html',self.views)
class Product_detail(Base):
    def get(self,request,slug):
        self.views['detailpro'] = Product.objects.filter(slug=slug)
        subcat_id = Product.objects.get(slug=slug).subcategory_id
        self.views['relate'] = Product.objects.filter(subcategory_id=subcat_id)
        self.views['product_review'] = Review.objects.filter(slug=slug)
        return render(request,'product-detail.html',self.views)
def review(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        star = request.POST['star']
        slug = request.POST['slug']
        comment = request.POST['comment']
        x = datetime.datetime.now()
        date = x.strftime("%C")
        data = Review.objects.create(
            name=name,
            email=email,
            star=star,
            slug=slug,
            comment=comment,
            date=date

        )
        data.save()
        return redirect(f'/detail/{slug}')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        if password == cpassword:
            if User.objects.filter(username = username).exists():
                messages.error(request,'The username is already taken.')
                return redirect('/signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'The email is already taken.')
                return redirect('/signup')
            else:
                user = User.objects.create_user(
                    username = username,
                    email = email,
                    password = password
                )
                user.save()
                return redirect('/signup')
        else:
            messages.error(request, 'The password does not match')
            return redirect('/signup')

    return render(request,'signup.html')

def dologin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            return redirect('/login')
    return render(request,'registration/login.html')

def dologout(request):
    logout(request)
    return render(request,'index.html')
class Car(Base):
    def get(self,request):
        s = 0
        username = request.user.username
        self.views['viewcart'] = Cart.objects.filter(username=username)
        for i in self.views['viewcart']:
            s = s + i.total
            self.views['sub_total'] = s
            self.views['delivery_charge'] = 50
            self.views['grand_total'] = s + 50
        return render(request,'cart.html',self.views)

def add_cart(request,slug):
    if Product.objects.filter(slug=slug).exists():
        username = request.user.username
        if Cart.objects.filter(username=username,slug=slug,checkout=False).exists():
            quantity = Cart.objects.get(slug=slug,username=username).quantity
            price = Product.objects.get(slug=slug).price
            discounted_price = Product.objects.get(slug=slug).discounted_price
            quantity = quantity + 1
            if discounted_price > 0 :
                total = quantity * discounted_price
            else :
                total = quantity * price
            Cart.objects.filter(username=username,slug=slug,checkout=False).update(quantity=quantity,total=total)
            return redirect('/car')
        else :
            price = Product.objects.get(slug=slug).price
            discounted_price = Product.objects.get(slug=slug).discounted_price
            if discounted_price > 0:
                total = discounted_price
            else:
                total = price
            data = Cart.objects.create(
                username=username,
                quantity=1,
                total=total,
                slug=slug,
                items=Product.objects.get(slug=slug)

            )
            data.save()
            return redirect('/car')

def reduce_quantity(request,slug):
    if Product.objects.filter(slug=slug).exists():
        username = request.user.username
        if Cart.objects.filter(username=username,slug=slug,checkout=False).exists():
            quantity = Cart.objects.get(slug=slug).quantity
            price = Product.objects.get(slug=slug).price
            discounted_price = Product.objects.get(slug=slug).discounted_price
            quantity = quantity - 1
            if discounted_price > 0 :
                total = quantity * discounted_price
            else :
                total = quantity * price
            Cart.objects.filter(username=username,slug=slug,checkout=False).update(quantity=quantity,total=total)
            return redirect('/car')
def delete_cart(request,slug):
    username = request.user.username
    if Cart.objects.filter(slug=slug, username=username).exists():
        Cart.objects.filter(slug=slug, username=username).delete()
        return redirect('/car')

class Check(Base):
    def get(self,request):
        s = 0
        username = request.user.username
        self.views['checkouts'] = Cart.objects.filter(username=username)
        for i in self.views['checkouts']:
            s = s + i.total
            self.views['sub_total'] = s
            self.views['delivery_charge'] = 50
            self.views['grand_total'] = s + 50
        return render(request,'checkout.html',self.views)
def orderform(request):
    if request.method == 'POST':
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id=uid)
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        phone = request.POST['phone']
        email = request.POST['email']
        post_code = request.POST['post_code']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        amount = request.POST['amount']

        data = Order.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            city=city,
            country=country,
            phone=phone,
            post_code=post_code,
            state=state,
            amount=amount

        )
        data.save()
    return render(request,'placeorder.html')