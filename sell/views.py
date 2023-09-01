from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .forms import verify_mobile_number,Add_product
from .models import Products,Orders
from django.contrib.auth.decorators import login_required
from profiles.models import User_details
from django.contrib import messages
# to store image
from django.core.files.storage import FileSystemStorage
#from .market_price import market_price as mp
from .market_price_location import market_price as mp
from profiles.views import profile

# Create your views here.
User = get_user_model()
mprice = mp()

@login_required
def orders(request,type=None,oid=None,stat=None):
    seller = User_details.objects.get(user_id =request.user.id)
    if type == 'products':
        
        quantity = dict()
        products = Products.objects.filter(seller = seller)
        m_price =dict()
        if products:
            for product in products:
                order = Orders.objects.filter(product_id = product.product_id)
                print(product.product_name,seller.district)
                val = mprice.price(product.product_name,seller.district)
                m_price[product.product_name] = val
               
            return render(request,'pages/sell.html',{'type':'products','products':products,'m_price':m_price,})
        else:
            return render(request,'pages/sell.html',{'type':'products'})
    elif type == 'orders':
        orders = Orders.objects.filter(seller = seller)
        if orders:
            users = User_details.objects.all()
            product = dict()
            pobj = Products.objects.filter(seller = seller)
            for p in pobj:
                product[p.product_id] = p.product_name
            status = dict()
            mobile = dict()
            for order in orders:
                for user in users:
                    if order.user == user.user:
                        mobile[order.user] = user.mobile
                if order.status == 'ordered':
                    status[order.order_id] = 'confirm'
                if order.status == 'confirmed':
                    status[order.order_id] = 'deliver'
                if order.status == 'delivered':
                    status[order.order_id] = 'delivered'    
            return render(request, 'pages/sell.html', {'type':type,'orders': orders,'mobile': mobile,'products':product,'status':status})
        else:
            return render(request, 'pages/sell.html',{'type':type})
    else:
    
        products = Products.objects.filter(seller = seller)
        if products:
            order = Orders.objects.filter(seller = seller)
            m_price =dict()
            for product in products:
                o = Orders.objects.filter(product_id = product.product_id)
                
                val = mprice.price(product.product_name,seller.district)
                m_price[product.product_name] = val
                    
            return render(request,'pages/sell.html',{'type':'products','products':products,'m_price':m_price,})
        else:
            return render(request,'pages/sell.html',{'type':'products'})
        
@login_required
def price_change(request,pid = 0):
    if pid == 0:
        if request.method =='POST':
            product =request.POST.get('product')
            price = request.POST.get('price')
            if price:
                
                product = Products.objects.get(product_id=int(product))
                product.price = price
                product.save(update_fields=['price'])
                return redirect('/sell/')
            else:
                messages.info(request,'enter the new price before submit')
                return redirect('/sell/')

    else:
            
        if request.method == 'POST':
            price = request.POST.get('price')
            product = Products.objects.get(product_id=pid)
            product.price = price
            product.save(update_fields=['price'])
            return redirect('/sell/')
        
        
def remove_product(request,pid=0):
    product = Products.objects.get(product_id=pid)
    if product:
        product.delete()
        return redirect('/sell/')
    
    else:
        return render(request, '404.html')
        

@login_required
def order_status(request,oid=None,stat=None):
    if oid and stat:
        order = Orders.objects.get(order_id = oid)
        if stat == 'ordered':
            order.status = 'confirmed'
        if stat =='confirmed':
            order.status = 'delivered'
        if stat == 'cancel':
            product = Products.objects.get(product_id = order.product_id.product_id)
            totqty = product.total_quantity + order.quantity
            product.total_quantity = totqty
            product.save(update_fields=['total_quantity'])
            order.delete()
            return redirect('/sell/orders/')
        order.save(update_fields=['status'])
        return redirect('/sell/orders/')

            
    

'''
@login_required
def verify_mobile(request):
    form = verify_mobile_number(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            mobile = form.cleaned_data.get('mobile')
            user = User.objects.get(id=request.user.id)
            seller_id = 100+request.user.id
            obj = Seller.objects.create(
                seller_id = seller_id,
                user = user,
                mobile = mobile,
            )
            obj.save()
            
            return HttpResponse('seller page')
    return render(request,'mobile.html',{'form':form})
'''

from django.core.files.storage import FileSystemStorage

@login_required
def add_product(request):
    products =['Amaranth leaves',
                'Amla',
                'Ash gourd',
                'Baby corn',
                'Banana flower',
                'Beetroot',
                'Bell Pepper (Capsicum)',
                'Bitter gourd',	
                'Bottlegourd',
                'Butter beans',
                'Broad beans (Fava beans, lima beans)',
                'Cabbage',	
                'Carrot',
                'Cauliflower',
                'Cluster beans',
                'Coconut (fresh)',
                'Colocasia leaves (Taro leaves)',
                'Colocasia roots (Taro roots)',
                'Coriander leaves (Cilantro)',
                'Corn',
                'Cucumber',
                'Curry leaves',
                'Dill leaves',
                'Drumsticks',
                'Eggplant (Brinjal or Aubergine)',
                'Brinjal ( Big )',
                'Elephant Yam',
                'Fenugreek leaves',
                'French Beans (Green beans)',
                'Garlic',
                'Ginger',
                'Green chili',
                'Green onion',
                'Green peas',
                'Ivy gourd',
                'Lemon',
                'Mango',
                'Mint leaves',
                'Mushroom',
                'Mustard leaves',
                'Okra (Ladies finger)',
                'Onion Big',
                'Onion Small',
                'Plantain (raw banana)',
                'Potato	',
                'Pumpkin',
                'Radish (Daikon)',
                'Ridge gourd',
                'Shallot (pearl onion)',
                'Snake gourd',
                'Sorrel leaves',
                'Spinach',
                'Sweet potato',
                'Tomato',
                'Apple washington',
                'Apple Simla',
                'Apple Green',
                'Apricot',
                'Avocado',
                'Banana Morris',
                'Banana Regular',
                'Banana other',
                'Cantaloupe (Musk melon)',
                'Custard apple',
                'Gooseberry',
                'Grapes (black)',
                'Grapes (green)',
                'Guava',
                'Jackfruit',
                'Lychee',
                'Mango, ripe',
                'Mango, unripe',
                'Orange',
                'Papaya',
                'Pears',
                'Pineapple',
                'Pomegranate',
                'Sapota',
                'Sugar cane',
                'Sweet lime',
                'Watermelon',
            ]
    
    if request.method == 'POST':
    
        name = request.POST.get('product_name')
        print(name)
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        seller_id = 'cus100'+str(request.user.id)
        seller = User_details.objects.get(seller_id=seller_id)
        obj = Products.objects.create(
            product_name = name,
            product_image = image if image else 'products/dummy.jpg',
            total_quantity = quantity,
            seller = seller,
            price = price,
        )
        
        obj.save() 
        return redirect('/sell')
    
    else:
        return render(request,'pages/add_product.html',{'products':products})
    

@login_required
def order(request,pid):
    product = Products.objects.get(product_id = pid)
    products = Products.objects.filter( seller = product.seller)
    
    if request.method == 'POST':
        oqty = int(request.POST.get('quantity'))
        product_id = pid
        if oqty == '':
            messages.info(request,'enter the quantity')
            return render(request,'pages/order.html',{'product':product,'products':products})
        elif oqty <= product.total_quantity:
            
            price = oqty*product.price
            seller = product.seller
            user = request.user
            oobj = Orders.objects.create(product_id = product, quantity =oqty, user = user,price=price,seller = seller)
            oobj.save()
            totqty = product.total_quantity - oqty
            product.total_quantity = totqty
            product.save(update_fields=['total_quantity'])
            user_details = User_details.objects.get(user = request.user)
            orders = Orders.objects.filter(user = request.user).order_by('date')
            return render(request,'pages/profile.html',{'userd':user_details,'type':'orders','orders':orders,})
        
            
        else:
            messages.info(request,f'{oqty}kg is not available.place order with less quantity!!')
            return render(request,'pages/order.html',{'product':product,'products':products})
    else:
        print(pid)
        return render(request,'pages/order.html',{'product':product,'products':products})
   



