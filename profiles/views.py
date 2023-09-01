from http.client import HTTPResponse
# for mail
from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail

import http,os

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from .forms import Registration, Loginform, PasswordResetForm
from .models import User_details,Qr
from django.contrib import messages
from .geopymod import locate,Find_distance
from .qrcodemod import Qr_code
from hashlib import sha256 as sha
import smtplib, ssl


from sell.models import Products,Orders
from django.utils.translation import gettext as _

#qr image download

from django.utils import translation

def set_lang(request,lang):
    next = request.get_full_path()
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    print(next)
    response = redirect(next)
    if request.method == 'GET':
        lang_code = lang
        if lang_code:
            if hasattr(request, 'session'):
                request.session['django_language'] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
            translation.activate(lang_code)
    return response

User = get_user_model()
url = '192.168.43.82:8000/'
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = User_details.objects.get(user = request.user)
            products = Products.objects.all()
            farmers = Products.objects.distinct('seller')
            d_products = Products.objects.distinct('product_name')
            distance = dict()
            fdist=ffarmer=fproduct = ''
            prod = list()
            f_dist =0
            fdist = request.POST.get('dist')
            ffarmer = request.POST.get('farmer')
            fproduct = request.POST.get('product')
            print(ffarmer,' : ',fproduct,':',fdist,)
            f_products = Products.objects.all()
            if fproduct!= 'all':
                f_products = Products.objects.filter(product_name = fproduct,)
            if ffarmer!= 'all':
                u = User.objects.get(username=ffarmer)
                ud = User_details.objects.get(user = u)
                f_products = Products.objects.filter( seller = ud )
            
            if fdist!= 'all':
                lat1 = user.latitude
                lon1 = user.longitude
                for product in f_products:
                    user1 = User_details.objects.get( user = product.seller)
                    lat2 = user1.latitude
                    lon2 = user1.longitude
                    fd = Find_distance(lat1,lon1,lat2,lon2)
                    dist = fd.distance()
                    print(dist)
                    if dist <= int(fdist):
                        prod.append(product)
            
            if not (prod):
                return render(request,'pages/home.html',{'dist':fdist,'fp':fproduct,'ff':ffarmer,'products':f_products,'farmers':farmers,'d_products':d_products,})   
            else:
                return render(request,'pages/home.html',{'dist':fdist,'fp':fproduct,'ff':ffarmer,'products':prod,'farmers':farmers,'d_products':d_products,})   
        else:
            return render(request,'pages/login.html')
    else:
                
        products = Products.objects.all().order_by('-total_quantity')
        users = User.objects.all()
        farmers = Products.objects.distinct('seller')
        d_products = Products.objects.distinct('product_name')
        
        
        return render(request,'pages/home.html',{'products':products,'farmers':farmers,'d_products':d_products,})


def RegistrationForm(request):
    
    if request.method == 'POST':
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        email = request.POST.get('email')
        village = request.POST.get('village')
        mobile = request.POST.get('mobile')
        if mobile:
            mobile = int(mobile)
        else:
            mobile = '--'
        city = request.POST.get('city')
        mandal = request.POST.get('mandal')
        district = request.POST.get('district')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pin = request.POST.get('pincode')
        eqs = User.objects.filter(email = email)
        if eqs.exists():
            messages.info(request,'email already exists')
            return render(request,'pages/registration.html')
        else:
            uqs = User.objects.filter(username = email )
            if uqs.exists():
                messages.info(request,'username already taken ')
                return render(request,'pages/registration.html')
            else:
                if password == password1:
                    obj = locate(village,city, mandal, district, state, country, pin)
                    lat , lon = obj.lat_lon()
                    x = email
                    user = User.objects.create_user(username=x,email=email,first_name=first_name,last_name=last_name,password=password)            
                    user.save()
                    suser = User.objects.get(id=user.id)
                    seller_id = str('cus100'+str(suser.id))
                    loc = User_details.objects.create(user=user,mobile = mobile, village=village,city=city,mandal=mandal,district=district,state=state,country=country,pin = pin,latitude= lat,longitude = lon,seller_id = seller_id,)
                    loc.save() 
                    urll = '192.168.43.82:8000/qr/'
                    username = first_name+last_name
                    st = username+email+password
                    key = sha(st.encode()).hexdigest()
                    qrobj = Qr_code()
                    qrimg = qrobj.gen_qr(urll,key)
                    qobj = Qr(user = user ,key = key, qr = qrimg)
                    qobj.save()
                    
                    # QR to mail
                    '''
                    from_email = 'vamseed123@gmail.com'
                    to_email = user.email
                    subject = 'qr code for login purposes'
                    body = 'you can use the following qrcode for login purposes.Do not share this qr code with anyone..!'
                    msg = EmailMessage(
                        subject,
                        body,
                        from_email=from_email,
                        to=[to_email]
                    )
                    qr = Qr.objects.get(user = user)
                    name = qr.qr.name
                    msg.attach_file(f'media/{name}')
                    msg.send()
                    print('qr code is sent successfully')
                    
                    '''
                    
                    #downloading qr
                    qr = Qr.objects.get(user = user)
                    f_fath = base_dir +"\media\qr" + f"\{qr.key}.png"
                    filename = f'QR_{qr.user.first_name}.png'
                    chunk_size = 8192
                    wrapper      = FileWrapper(open(f_fath,'rb'),chunk_size)  # img.file returns full path to the image
                    response     = StreamingHttpResponse(wrapper ,content_type='image/png')
                    response['Content-Length']      = os.path.getsize(f_fath)    
                    response['Content-Disposition'] = "attachment; filename=%s" %  filename
                    return response
                else:
                    messages.info(request,'re-enter the password')
                    return render(request,'pages/registration.html')
    else:
        return render(request,'pages/registration.html')
            
    
    
def login_view(request):
    form = Loginform(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(request,username=username,password=password)
            if user != None:
                auth.login(request,user)
                #return HTTPResponse('!!you are logged in successfully')
                return redirect('/')
            else:
                messages.info(request,'invalid username or password')
                return render(request,'pages/login.html',{'form':form,})
    else:
        return render(request,'pages/login.html',{'form':form})


def logout_view(request):
    auth.logout(request)
    return redirect('/')

#method for

def qr_login(request, key=None):
    if key == None:
        messages.info(request,'invalid qrcode user your credentials instead')
        return render(request,'login.html')
    else:
        kobj = Qr.objects.get(key = key)
        uobj = User.objects.get(id= kobj.user_id)
        #user = auth.authenticate(request,username=uobj.username, password = uobj.password)
        if uobj != None:
            auth.login(request,uobj)
            return redirect('/sell/')
        else:
            messages.info(request,'invalid qrcode user your credentials instead')
            return render(request,'login.html')
        

#testing Find_distance code in geopymod.py
@login_required
def find_distance(request):
    cus = User_details.objects.get(user_id=request.user.id)
    users = User_details.objects.all()
    out = {}
    for user in users:
        if user.user_id != cus.user_id:
            dobj = Find_distance(cus.latitude,cus.longitude,user.latitude,user.longitude)
            dis = dobj.distance()
            out[(User.objects.get(id=user.user_id)).username] =dis

    return render(request,'home.html',{'distance':out})

@login_required
def qr(request):
    qobj = Qr.objects.get(user_id=request.user.id)
    pattern = url+qobj.key
    gen = Qr_code()
    img = gen.gen_qr(pattern)
    return render(request,'home.html',{'img':img})



# need to update in the future
def password_reset_request(request):
    password_reset_form = PasswordResetForm(request.POST or None)
    if request.method == "POST":
        
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
					"email":user.email,
					'domain':'192.168.43.82:8000',
					'site_name': 'Project_a',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'vamseed123@gmail.com' , [user.email])
                    except Exception as e:
                        messages.info(request,e)
                        return render(request,'404.html')
                    messages.info(request,"We've emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly. If you don't receive an email, please make sure you've entered the address you registered with, and check your spam folder")
                    return render(request,'pages/forgot-password.html',{"password_reset_form":password_reset_form})
            else:
                messages.info(request,'Invalid email there is no account with that mail address')
                return render(request,"pages/forgot-password.html", {"password_reset_form":password_reset_form})
    return render(request, "pages/forgot-password.html",{"password_reset_form":password_reset_form})
    
# resetting the password

@login_required
def profile(request,info=None):
    userd = User_details.objects.get(user = request.user)
    
    if info == 'qr':
        qobj = Qr.objects.get(user = request.user)
        img = qobj.qr
        print(img)
        return render(request,'pages/profile.html',{'userd':userd,'type':'qr','qr':qobj,})  
    else:
        
        orders = Orders.objects.filter(user = request.user).order_by('date')
        mobile = dict()
        pname = dict()
        for order in orders:
            p = Products.objects.get(product_id = order.product_id.product_id )
            pname[order.order_id] = p.product_name
            u = User_details.objects.get(seller_id = order.seller.seller_id)
            mobile[order.order_id] = u.mobile
        return render(request,'pages/profile.html',{'userd':userd,'type':'orders','orders':orders,})
    
@login_required
def edit_profile(request):
    userd = User_details.objects.get(user=request.user.id)
    if request.method == 'POST':
    
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        email = request.POST.get('email')
        village = request.POST.get('village')
        mobile = request.POST.get('mobile')
        city = request.POST.get('city')
        mandal = request.POST.get('mandal')
        district = request.POST.get('district')
        state = request.POST.get('state')
        country = request.POST.get('country')
        pin = request.POST.get('pincode')
        uqs = User.objects.filter(username = email )
        obj = locate(village,city, mandal, district, state, country, pin)
        lat , lon = obj.lat_lon()
        user = User.objects.get(id = request.user.id)  
        user.username= email
        user.email=email
        user.first_name=first_name
        user.last_name=last_name
        user.save()
        suser = User.objects.get(id=user.id)
        seller_id = str('cus100'+str(suser.id))
        
        loc = User_details.objects.get(user=request.user.id)
        loc.mobile = mobile
        loc.village=village
        loc.city=city
        loc.mandal=mandal
        loc.district=district
        loc.state=state
        loc.country=country
        loc.pin = pin
        loc.latitude= lat
        loc.longitude = lon
        loc.seller_id = seller_id
        loc.save() 
        urll = '192.168.43.82:8000/qr/'
        username = first_name+last_name
        st = username+email+request.user.password
        key = sha(st.encode()).hexdigest()
        qrobj = Qr_code()
        qrimg = qrobj.gen_qr(urll,key)
        qobj = Qr(user = user ,key = key, qr = qrimg)
        qobj.save()
        
        from_email = 'vamseed123@gmail.com'
        to_email = user.email
        subject = 'qr code for login purposes'
        body = 'you can use the following qrcode for login purposes.Do not share this qr code with anyone..!'
        msg = EmailMessage(
            subject,
            body,
            from_email=from_email,
            to=[to_email]
        )
        qr = Qr.objects.get(user = user)
        name = qr.qr.name
        msg.attach_file(f'media/{name}')
        msg.send()
        print('qr code is sent successfully')
        
        
        return redirect('/profile/')
    
        
    else:
        userd = User_details.objects.get(user=request.user.id)
        return render(request,'pages/editprofile.html',{'userd':userd})

def cancel_order(request,oid=None):
    order = Orders.objects.get(order_id = oid)
    product = Products.objects.get(product_id = order.product_id.product_id)
    totqty = product.total_quantity + order.quantity
    product.total_quantity = totqty
    product.save(update_fields=['total_quantity'])
    order.delete()
    return redirect('/profile/')


#download QR 

from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes,os

@login_required
def download_qr(request):
    user = User.objects.get(id = request.user.id)
    img = Qr.objects.get(user = user)
    f_fath = base_dir +"\media\qr" + f"\{img.key}.png"
    filename = f'QR_{img.user.first_name}.png'
    chunk_size = 8192
    wrapper      = FileWrapper(open(f_fath,'rb'),chunk_size)  # img.file returns full path to the image
    response     = StreamingHttpResponse(wrapper ,content_type='image/png')
    response['Content-Length']      = os.path.getsize(f_fath)    
    response['Content-Disposition'] = "attachment; filename=%s" %  filename
    return response
    
  


def qr_mail(request):

    subject = 'qr code for login purposes'
    body = 'you can use the following qrcode for login purposes.Do not share this qr code with anyone..!'

    from_email = 'vamseed123@gmail.com'
    user = User.objects.get(id = request.user.id)
    det = profile(request)
    msg = EmailMessage(
        subject,
        body,
        from_email=from_email,
        to=[user.email],
    )
    qr = Qr.objects.get(user = user)
    name = qr.qr.name
    msg.attach_file(f'media/{name}')
    msg.send()
    

    return render(request,'pages/profile.html',{'userd':det.userd,'type':'qr','qr':det.qobj,})


def base(request):
    return render(request,'404.html')

def market_price (request):
    return HttpResponse('marlet prce finder')