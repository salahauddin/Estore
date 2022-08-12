from django.shortcuts import render,redirect
from .models import product,color,Sizes,Productattribute,Brand,category
from django.http import JsonResponse
from django.template.loader import render_to_string
from .forms import SignUpForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required

#paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.
def index(request):
    data=product.objects.filter(isFeatured=True).order_by('-id')[:5]
    return render(request,'index.html',{'data':data})

def Category_list(request):
    cat=category.objects.all().order_by('-id')
    return render(request,'category.html',{'data':cat})

def Category_product_list(request,id):
    id1=int(id)
    cat=category.objects.get(id=id1)
    data=product.objects.filter(category=cat)
    return render(request,'catpro.html',{'data':data})

def Brand_list(request):
    brand=Brand.objects.all().order_by('-id')
    return render(request,'brand.html',{'data':brand})

def Brand_product_list(request,id):
    id1=int(id)
    br=Brand.objects.get(id=id1)
    data=product.objects.filter(brand=br)
    return render(request,'catpro.html',{'data':data})
    

def productlist(request):
    data=product.objects.filter(isFeatured=True).order_by('-id')
    return render(request,'productlist.html',{'data':data})


def filter_data(request):
	colors=request.GET.getlist('color[]')
	categories=request.GET.getlist('category[]')
	brands=request.GET.getlist('brand[]')
	sizes=request.GET.getlist('size[]')
	allProducts=product.objects.all().order_by('-id').distinct()
	if len(colors)>0:
		allProducts=allProducts.filter(productattribute__color__id__in=colors).distinct()
	if len(categories)>0:
		allProducts=allProducts.filter(category__id__in=categories).distinct()
	if len(brands)>0:
		allProducts=allProducts.filter(brand__id__in=brands).distinct()
	if len(sizes)>0:
		allProducts=allProducts.filter(productattribute__size__id__in=sizes).distinct()
	t=render_to_string('ajax/product-list.html',{'data':allProducts})
	return JsonResponse({'data':t})


def products(request,id):
    id=int(id)
    product1=product.objects.get(id=id)
    related_products=product.objects.filter(category=product1.category).exclude(id=id)[:4]
    Color=Productattribute.objects.filter(product=product1).values('color__color_code','color__id').distinct()
    sizes=Productattribute.objects.filter(product=product1).values('id','size__id','size__size','price','color__id').distinct()
    return render(request,'product.html',{'data':product1,'data1':related_products,'colors':Color,'sizes':sizes})

def addtocart(request):
   # del request.session['cartdata']
    id=str(request.GET['id'])
    total=int(request.GET['qty'])*float(request.GET['price'])
    cartdata={}
    cartdata[id]={
        'title':request.GET['title'],
        'qty':int(request.GET['qty']),
        'price':float(request.GET['price']),
      #  'total':float(total)
        } 
    print("cartdata")
    if 'cartdata' in request.session :
        if(id in request.session['cartdata']):
            cdata=request.session['cartdata']
            cdata[id]['qty']=int(request.GET['qty'])
            request.session['cartdata']=cdata
           # request.session['cartdata']['id']['total']=float(request.session['cartdata']['id']['qty']*float(request.session['price']))
        else:
            cdata=request.session['cartdata']
            cdata.update(cartdata)
            request.session['cartdata']=cdata
    else:
        request.session['cartdata']=cartdata
    
    return JsonResponse({'data':request.session['cartdata'], 'totalitems':len(request.session['cartdata'])})

def cart(request):
    total=0
    if 'cartdata' in request.session:
        for pid,var in request.session['cartdata'].items():
            total+=var['qty']*float(var['price'])
        return render(request,'cart.html',{'data':request.session['cartdata'], 'totalitems':len(request.session['cartdata']),'total':total})
    else:
        return render(request,'cart.html',{'data':'', 'totalitems':0,'total':0})               
    
def updatecart(request):
    id=str(request.GET['id'])
    qty=int(request.GET['qty'])
    cart=request.session['cartdata']
    cart[id]['qty']=qty
    total=0
    for pid,item in cart.items():
        
        total=cart[pid]['price']*qty
    request.session['cartdata']=cart
    t=render_to_string('Ajax/cart-list.html',{'data':request.session['cartdata'], 'totalitems':len(request.session['cartdata']),'total':total})
    return JsonResponse({'data':t})

def signup(request):
	if request.method=='POST':
		form=SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			pwd=form.cleaned_data.get('password1')
			user=authenticate(username=username,password=pwd)
			login(request, user)
			return redirect('index')
	form=SignUpForm
	return render(request, 'registration/Register.html',{'form':form})


#https://www.sandbox.paypal.com/
@login_required()
def checkout(request):
    amt=0
    
    if 'cartdata' in request.session:
        for pid,val in request.session['cartdata'].items():
            amt+=float(val['qty']*val['price'])
    
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': amt,
        'item_name': 'OrderNo-232323',
        'invoice': 'INV-333321',
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,reverse('payment_cancelled')),
        
		}
    form = PayPalPaymentsForm(initial=paypal_dict)
        
    return render(request,'checkout.html',{'data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total':amt,'form':form})
    
#@csrf_exempt
def payment_done(request):
	returnData=request.POST
	return render(request, 'payment-success.html',{'data':returnData})


@csrf_exempt
def payment_canceled(request):
	return render(request, 'payment-fail.html')

    
