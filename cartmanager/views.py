from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from prodectmanager.models  import Category, Subcategory,BlogModel, wishlist, orders, orderProdects,  Prodects,categoryDisplay,Sitesettings, Sliders, specialofferProdects, gallery as gallerymodel
from cart.cart import Cart
from django.conf import settings
import razorpay
from usermanager.models import zipcodes, shippingaddress
from datetime import datetime
import datetime as dt
from json import dumps
from datetime import timedelta, date
import uuid
from django import template
register = template.Library()

# Create your views here.



def home(request):
	
	sitesettings = Sitesettings.objects.all()
	newprodects = Prodects.objects.filter(position = 'new', state=1)
	categoroies =  Category.objects.order_by('-id')[:5]
	todaydeals = Prodects.objects.filter(position = 'todaydeals', state=1).order_by('-id')[:12]
	bestseller = Prodects.objects.filter(position = 'bestseller', state=1).order_by('-id')[:5]
	featuredproducts = Prodects.objects.filter(position = 'featuredproducts', state=1).order_by('-id')[:5]
	allcategoroies =  Category.objects.all()
	categoryDisplaylist = categoryDisplay.objects.all().order_by("position")
	bloddata = BlogModel.objects.all()
	sp = specialofferProdects.objects.all()
	

	catlist = []
	menulist =[]
	allmenues = []

	for menu in allcategoroies:
		catid = menu.id
		for s in Subcategory.objects.filter(cat_id=int(menu.id)):
			
			allmenues.append({'menuid':s.cat_id , 'submenu_id' : s.id, "submenu_name":s.subcat_name})

		menulist.append({"mainmenu_id":menu.id, "mainmenu_name":menu.cat_name, "submenus":allmenues})
		allmenues= []	


	for c in categoroies:
		cname = c.cat_name
		catimg = c.catimage
		catlist.append({ 
			'catid':c.id,
			'name':cname,
			'image': catimg,
			})

	data = {
	"title": sitesettings[0].site_title,
	"phone":sitesettings[0].site_phone,
	"email":sitesettings[0].site_email,
	"logo":sitesettings[0].site_logo,
	"copyrights":sitesettings[0].copyright,
	'sliders':Sliders.objects.filter(status=1),
	"newprodects": newprodects,
	'catdisplay'       : catlist,
	'todaydeals':todaydeals,
	"bestseller":bestseller,
	"featuredproducts":featuredproducts,
	"menulist":menulist,
	"categoryDisplaylist":categoryDisplaylist,
	"specialofferProdects" : sp,
	'bloddata':bloddata,
	
	}
	
	return render(request, "home.html",  data)
	#return HttpResponse("request.POST")

def productsingle(request):
	sitesettings = Sitesettings.objects.all()
	newprodects = Prodects.objects.filter(position = 'new', state=1)
	categoroies =  Category.objects.order_by('-id')[:5]
	todaydeals = Prodects.objects.filter(position = 'todaydeals', state=1).order_by('-id')[:12]
	bestseller = Prodects.objects.filter(position = 'bestseller', state=1).order_by('-id')[:5]
	featuredproducts = Prodects.objects.filter(position = 'featuredproducts', state=1).order_by('-id')[:5]
	allcategoroies =  Category.objects.all()
	categoryDisplaylist = categoryDisplay.objects.all().order_by("position")
	bloddata = BlogModel.objects.all()
	sp = specialofferProdects.objects.all()
	featuredproducts = {}
	relatedprodects = {}



	prodect = {}
	if request.GET.get('pid', False):
		prodect = Prodects.objects.get(id = request.GET['pid'])
		featuredproducts = Prodects.objects.filter(position = 'featuredproducts', state=1).order_by('-id')[:5]
		relatedprodects = Prodects.objects.filter(cat_id = prodect.cat_id,subcat_id=prodect.cat_id, state=1).exclude(id= prodect.id ).order_by('-id') 
	catlist = []
	menulist =[]
	allmenues = []

	for menu in allcategoroies:
		catid = menu.id
		for s in Subcategory.objects.filter(cat_id=int(menu.id)):
			
			allmenues.append({'menuid':s.cat_id , 'submenu_id' : s.id, "submenu_name":s.subcat_name})

		menulist.append({"mainmenu_id":menu.id, "mainmenu_name":menu.cat_name, "submenus":allmenues})
		allmenues= []	


	for c in categoroies:
		cname = c.cat_name
		catimg = c.catimage
		catlist.append({ 
			'catid':c.id,
			'name':cname,
			'image': catimg,
			})


	
	
	data = {
	"title":sitesettings[0].site_title,
	"phone":sitesettings[0].site_phone,
	"email":sitesettings[0].site_email,
	"logo":sitesettings[0].site_logo,
	"copyrights":sitesettings[0].copyright,
	'sliders':Sliders.objects.filter(status=1),
	"newprodects": newprodects,
	'catdisplay'       : catlist,
	'todaydeals':todaydeals,
	"bestseller":bestseller,
	"featuredproducts":featuredproducts,
	"menulist":menulist,
	"categoryDisplaylist":categoryDisplaylist,
	"specialofferProdects" : sp,
	'bloddata':bloddata,
	"prodect":prodect,
	'relatedprodects':relatedprodects,	
	"featuredproducts":featuredproducts,
	
	}
	

	return render(request, "product_single.html",  data)
	pass;

def allprodects(request):
	cart = request.session.get(settings.CART_SESSION_ID)
	categoroies =  Category.objects.order_by('-id')
	allcategoroies =  Category.objects.all()
	selectedCat = '';
	sitesettings = Sitesettings.objects.all()
	selectedCat =''



	catlist = []
	menulist =[]
	allmenues = []

	for menu in allcategoroies:
		catid = menu.id
		for s in Subcategory.objects.filter(cat_id=int(menu.id)):
			
			allmenues.append({'menuid':s.cat_id , 'submenu_id' : s.id, "submenu_name":s.subcat_name})

		menulist.append({"mainmenu_id":menu.id, "mainmenu_name":menu.cat_name, "submenus":allmenues})
		allmenues= []	

	for c in categoroies:		
		cname = c.cat_name
		catimg = c.catimage
		catlist.append({
		'catid':c.id,
        'name':cname,
        'image': catimg, })
	prodects = Prodects.objects.filter( state=1)
	if  request.GET.get("catid", False):
		selectedCat =  Category.objects.filter(id=request.GET['catid']  )[0].cat_name
		prodects = Prodects.objects.filter(cat_id = request.GET['catid'], state=1).order_by('-id')
	if 	 request.GET.get("submenuid", False):
		subcatageryname= Subcategory.objects.get(id=request.GET.get("submenuid", False))
		selectedCat =  selectedCat =  Category.objects.filter(id=request.GET['catid'])[0].cat_name
		prodects = Prodects.objects.filter(cat_id = request.GET['catid'], subcat_id = request.GET['submenuid'],state=1).order_by('-id')


	
	cart = Cart(request)
	
	data = {
	"title":sitesettings[0].site_title,
	"phone":sitesettings[0].site_phone,
	"email":sitesettings[0].site_email,
	"logo":sitesettings[0].site_logo,
	"copyrights":sitesettings[0].copyright,
	"menulist":menulist,
	'sliders':Sliders.objects.filter(status=1),
	 'selectedCat':selectedCat,
	  'categoroies':categoroies, 'selectedCat':selectedCat, "prodects":prodects,
	  "subcatageryname":subcatageryname}
	return render(request, "shop.html",  data)


def updatecart(request):
	 
	cart = request.session.get(settings.CART_SESSION_ID)
	for key, value in cart.items():
		if int(value['product_id']) ==  int(request.GET['pid']):
			cart[key]['quantity'] = int(request.GET['quantity'])
			request.session[settings.CART_SESSION_ID] = cart
			request.session.modified = True
			#print(cart[key])

	return HttpResponse(cart);

def cart_add(request, id):
	cart = Cart(request)
	product = Prodects.objects.get(id=id)
	cart.add(product=product)
	cart = request.session.get(settings.CART_SESSION_ID)
	redirect_to = request.GET.get('next', '/')	
	return redirect(redirect_to)

def cart_add_multy(request):
	cart = Cart(request)
	pid = request.GET.get("pid", '')
	product = Prodects.objects.get(id=pid)
	quantity =  int(request.GET.get("quantity", ''))
	cart.add(product=product,quantity=quantity)
	return HttpResponse(quantity);

#@login_required(login_url="/login")
def item_clear(request, id):
	
    cart = Cart(request)
    product = Prodects.objects.get(id=id)
    cart.remove(product)
    if(request.GET.get('next', None)):
    	redirect_to ="/"+request.GET.get('next', None)
    	return redirect(redirect_to)
    	
    else:
    	return redirect('/');
    	#return redirect("cart_detail")
    return redirect('/');


#@login_required(login_url="/login")
def itemincrement(request):
	id = request.GET['id'];
	cart = Cart(request)
	product = Prodects.objects.get(id=id)
	if request.GET.get('mlt'):
		for l in  range(0,request.GET.get('mlt')):
			cart.add(product=product)
	else :
		cart.add(product=product)
	return redirect("cart_detail")


#@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Prodects.objects.get(id=id)
    
    cart.decrement(product=product)
    return redirect("cart_detail")


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("/")


#@login_required(login_url="/login/?next=cartdetail")
def cart_detail(request):
	stotal = Cart(request)
	toataoitems = len(list(stotal.cart.items()) )
	cartisEmpty = False;
	if(toataoitems ==0):
		cartisEmpty = True

	stotal.totalamount()
	sitesettings = Sitesettings.objects.all()
	newprodects = Prodects.objects.filter(position = 'new',state=1)
	categoroies =  Category.objects.order_by('-id')[:5]
	todaydeals = Prodects.objects.filter(position = 'todaydeals',state=1).order_by('-id')[:8]
	bestseller = Prodects.objects.filter(position = 'bestseller',state=1).order_by('-id')[:5]
	featuredproducts = Prodects.objects.filter(position = 'featuredproducts',state=1).order_by('-id')[:5]
	allcategoroies =  Category.objects.all()
	categoryDisplaylist = categoryDisplay.objects.all().order_by("position")
	bloddata = BlogModel.objects.all()
	sp = specialofferProdects.objects.all()
	

	catlist = []
	menulist =[]
	allmenues = []

	for menu in allcategoroies:
		catid = menu.id
		for s in Subcategory.objects.filter(cat_id=int(menu.id)):
			
			allmenues.append({'menuid':s.cat_id , 'submenu_id' : s.id, "submenu_name":s.subcat_name})

		menulist.append({"mainmenu_id":menu.id, "mainmenu_name":menu.cat_name, "submenus":allmenues})
		allmenues= []	


	for c in categoroies:
		cname = c.cat_name
		catimg = c.catimage
		catlist.append({ 
			'catid':c.id,
			'name':cname,
			'image': catimg,
			})

	data = {
	"title":sitesettings[0].site_title,
	"phone":sitesettings[0].site_phone,
	"email":sitesettings[0].site_email,
	"logo":sitesettings[0].site_logo,
	"copyrights":sitesettings[0].copyright,
	'sliders':Sliders.objects.filter(status=1),
	"newprodects": newprodects,
	'catdisplay'       : catlist,
	'todaydeals':todaydeals,
	"bestseller":bestseller,
	"featuredproducts":featuredproducts,
	"menulist":menulist,
	"categoryDisplaylist":categoryDisplaylist,
	"specialofferProdects" : sp,
	'bloddata':bloddata,
	"cartisEmpty": cartisEmpty	
	}
	
	return render(request, 'cart_detail_new.html', data)

@login_required(login_url="/login/?next=checkout")
def checkout(request):
	data = {}
	sitesettings = Sitesettings.objects.all()
	allcategoroies =  Category.objects.all()
	catlist = []
	menulist =[]
	allmenues = []
	for menu in allcategoroies:
			catid = menu.id
			for s in Subcategory.objects.filter(cat_id=int(menu.id)):
				allmenues.append({'menuid':s.cat_id , 'submenu_id' : s.id, "submenu_name":s.subcat_name})

			menulist.append({"mainmenu_id":menu.id, "mainmenu_name":menu.cat_name, "submenus":allmenues})
			allmenues= []
	userAddress = shippingaddress.objects.filter(userid=request.user.id).first()	 
	data = {
	    
	"title":sitesettings[0].site_title,
	"phone":sitesettings[0].site_phone,
	"email":sitesettings[0].site_email,
	"logo":sitesettings[0].site_logo,
	"copyrights":sitesettings[0].copyright,
		"menulist":menulist,
		"address":userAddress	}
	return render(request, 'checkout.html', data)
	
	
def payment(request):	
	totalPay =   request.session['totalPay'] = {} 
	if request.user.is_authenticated:	
		stotal = Cart(request)
		#stotal.totalamount()
		cart = request.session.get(settings.CART_SESSION_ID)

		sitesettings = Sitesettings.objects.all()
		newprodects = Prodects.objects.filter(position = 'new',state=1)
		categoroies =  Category.objects.order_by('-id')[:5]
		todaydeals = Prodects.objects.filter(position = 'todaydeals',state=1).order_by('-id')[:5]
		bestseller = Prodects.objects.filter(position = 'bestseller',state=1).order_by('-id')[:5]
		featuredproducts = Prodects.objects.filter(position = 'featuredproducts',state=1).order_by('-id')[:5]
		allcategoroies =  Category.objects.all()
		catlist = []
		menulist =[]
		allmenues = []
		for menu in allcategoroies:
			catid = menu.id
			for s in Subcategory.objects.filter(cat_id=int(menu.id)):
				allmenues.append({'menuid':s.cat_id , 'submenu_id' : s.id, "submenu_name":s.subcat_name})

			menulist.append({"mainmenu_id":menu.id, "mainmenu_name":menu.cat_name, "submenus":allmenues})
			allmenues= []


		for c in categoroies:
			cname = c.cat_name
			catimg = c.catimage
			catlist.append({
				'catid':c.id,
				'name':cname,
				'image': catimg,
				})
	
		 
			



		totalPrice = 0
		for key, value in cart.items():
			totalPrice = int(cart[key]['quantity'])*int(cart[key]['price'])+totalPrice

		totalPrice = totalPrice*100
		
		for c in categoroies:
	   		cname = c.cat_name
	   		catimg = c.catimage
	   		catlist.append({
			'catid':c.id,
	        'name':cname,
	        'image': catimg, })
		slider = Sliders.objects.filter(status=1).order_by('-id')[:1]
		#client = razorpay.Client(auth=("rzp_test_oglxGr4tnsZpuY","NpiY7ldBj4HjwLSavgRKenGp"))
		client = razorpay.Client(auth=("rzp_live_API4QrHXwnLRwt", "NpiY7ldBj4HjwLSavgRKenGp"))
		
		receiptId = str(request.user.id)+str(uuid.uuid1())[:5]
		DATA ={
		'amount'           : totalPrice,
	    'currency'         : "INR",
	    'receipt'          : receiptId,
		}
		request.session['totalPay'] = {'totalpay':totalPrice, "info":DATA }
		p = client.order.create(data=DATA)
		data = {
		"title":sitesettings[0].site_title,
		"phone":sitesettings[0].site_phone,
		"email":sitesettings[0].site_email,
		"logo":sitesettings[0].site_logo,
		"copyrights":sitesettings[0].copyright,
		'sliders':slider,
		"newprodects": newprodects,
		"menulist":menulist,
		'catdisplay' : catlist,
		'todaydeals':todaydeals,
		"bestseller":bestseller,
		"featuredproducts":featuredproducts,
		'totalamount':totalPrice,
		'orderid':p['id']
		}
	return render(request, 'payment.html', data)
def pamentSucess(request):
	cart = request.session.get(settings.CART_SESSION_ID)
	orderid = str(request.user.id)+str(uuid.uuid1())[:5]+"@"+request.GET.get("pamentId","")

	if not cart:
		return redirect("/")
	orderdata = request.session.get('orderdata') 
	
	subtotal = 0
	for key, value in cart.items():
		st = int(cart[key]['quantity'])*int(cart[key]['price'])+subtotal
		subtotal = st+subtotal

	shippingAddrasString = orderdata['fname']+"**"+orderdata['lasttname']+"**"+orderdata['email']+"**"+orderdata['phone']+"**"+orderdata['flat']+"**"+orderdata['address']+"**"+orderdata['city']+"**"+orderdata["state"]+"**"+orderdata["zipcode"]
	
	prodectaddedList = ''
	for key, value in cart.items():
		#totalPrice = int(cart[key]['quantity'])*int(cart[key]['price'])
		prodectaddedList +=cart[key]['prodect_adby']+", "
		orderProdects(userId =request.user.id,
			orderId = orderid ,
			prodectId =cart[key]['product_id'],
			prodectName =cart[key]['name'] ,
			prodectPrice =cart[key]['price'] ,
			prodectImage  =cart[key]['image'] ,
			quantity =cart[key]['quantity'],
			prodect_addedby=prodectaddedList).save();
	orders(userId  = request.user.id, 
		username=orderdata['fname']+"__"+orderdata['lasttname'], 
		phone =   orderdata['phone'], 
		email =   orderdata['email'], 
		orderId = orderid,
		totalPrice = orderdata['totalprice'],
		subtotalPrice = orderdata['subtotal'],
		shippingprice  = orderdata['sprice'],
		orderDate   = date.today(),
		develiveryDate = date.today() + timedelta(days=10)  ,
		shippingAddras = shippingAddrasString,
		orderState  = 1,
		odertype = 1,
		prodect_addedby = prodectaddedList
		).save()
	
	#print(request.GET)
	cart.clear()
	data = {"orderdata":orderdata,'orderId' : orderid, "cart":cart,"orderDate":date.today(), 'develiveryDate' : date.today() + timedelta(days=10) }
	return render(request, 'sucess.html', data)

	

def blog(request):	
	request.session.modified = True
	sitesettings = Sitesettings.objects.all()
	newprodects = Prodects.objects.filter(position = 'new',state=1)
	categoroies =  Category.objects.order_by('-id')[:5]
	todaydeals = Prodects.objects.filter(position = 'todaydeals',state=1).order_by('-id')[:12]
	bestseller = Prodects.objects.filter(position = 'bestseller',state=1).order_by('-id')[:5]
	featuredproducts = Prodects.objects.filter(position = 'featuredproducts',state=1).order_by('-id')[:5]
	allcategoroies =  Category.objects.all()
	categoryDisplaylist = categoryDisplay.objects.all().order_by("position")
	bloddata = BlogModel.objects.all()
	sp = specialofferProdects.objects.all()
	

	catlist = []
	menulist =[]
	allmenues = []
	for menu in allcategoroies:
		catid = menu.id
		for s in Subcategory.objects.filter(cat_id=int(menu.id)):			
			allmenues.append({'menuid':s.cat_id , 'submenu_id' : s.id, "submenu_name":s.subcat_name})

		menulist.append({"mainmenu_id":menu.id, "mainmenu_name":menu.cat_name, "submenus":allmenues})
		allmenues= []	


	for c in categoroies:
		cname = c.cat_name
		catimg = c.catimage
		catlist.append({ 
			'catid':c.id,
			'name':cname,
			'image': catimg,
			})
	redirect_to = request.GET.get('next', None)
	if(redirect_to):
		redirect_path= "/login/?next="+redirect_to
	else:
		redirect_path= '/login/'


	users = {}
	data = {"redirect_path":redirect_path,
	"title":sitesettings[0].site_title,
	"phone":sitesettings[0].site_phone,
	"email":sitesettings[0].site_email,
	"logo":sitesettings[0].site_logo,
	"copyrights":sitesettings[0].copyright,
	'sliders':Sliders.objects.filter(status=1),
	"newprodects": newprodects,
	'catdisplay'       : catlist,
	'todaydeals':todaydeals,
	"bestseller":bestseller,
	"featuredproducts":featuredproducts,
	"menulist":menulist,
	"categoryDisplaylist":categoryDisplaylist,
	"specialofferProdects" : sp,
	'bloddata':bloddata,
	
	}
 
	 




	return render(request, 'blog.html', data)

def contact(request):
	sitesettings = Sitesettings.objects.all()
	newprodects = Prodects.objects.filter(position = 'new',state=1)
	categoroies =  Category.objects.order_by('-id')[:5]
	todaydeals = Prodects.objects.filter(position = 'todaydeals',state=1).order_by('-id')[:12]
	bestseller = Prodects.objects.filter(position = 'bestseller',state=1).order_by('-id')[:5]
	featuredproducts = Prodects.objects.filter(position = 'featuredproducts',state=1).order_by('-id')[:5]
	allcategoroies =  Category.objects.all()
	categoryDisplaylist = categoryDisplay.objects.all().order_by("position")
	bloddata = BlogModel.objects.all()
	sp = specialofferProdects.objects.all()
	catlist = []
	menulist =[]
	allmenues = []

	for menu in allcategoroies:
		catid = menu.id
		for s in Subcategory.objects.filter(cat_id=int(menu.id)):
			
			allmenues.append({'menuid':s.cat_id , 'submenu_id' : s.id, "submenu_name":s.subcat_name})

		menulist.append({"mainmenu_id":menu.id, "mainmenu_name":menu.cat_name, "submenus":allmenues})
		allmenues= []	


	for c in categoroies:
		cname = c.cat_name
		catimg = c.catimage
		catlist.append({ 
			'catid':c.id,
			'name':cname,
			'image': catimg,
			})

	data = {
	"title":sitesettings[0].site_title,
	"phone":sitesettings[0].site_phone,
	"email":sitesettings[0].site_email,
	"logo":sitesettings[0].site_logo,
	"copyrights":sitesettings[0].copyright,
	'sliders':Sliders.objects.filter(status=1),
	"newprodects": newprodects,
	'catdisplay'       : catlist,
	'todaydeals':todaydeals,
	"bestseller":bestseller,
	"featuredproducts":featuredproducts,
	"menulist":menulist,
	"categoryDisplaylist":categoryDisplaylist,
	"specialofferProdects" : sp,
	'bloddata':bloddata,
	
	}
	
	return render(request, 'contact.html', data)
def aboutus(request):
	sitesettings = Sitesettings.objects.all()
	newprodects = Prodects.objects.filter(position = 'new',state=1)
	categoroies =  Category.objects.order_by('-id')[:5]
	todaydeals = Prodects.objects.filter(position = 'todaydeals',state=1).order_by('-id')[:12]
	bestseller = Prodects.objects.filter(position = 'bestseller',state=1).order_by('-id')[:5]
	featuredproducts = Prodects.objects.filter(position = 'featuredproducts',state=1).order_by('-id')[:5]
	allcategoroies =  Category.objects.all()
	categoryDisplaylist = categoryDisplay.objects.all().order_by("position")
	bloddata = BlogModel.objects.all()
	sp = specialofferProdects.objects.all()
	catlist = []
	menulist =[]
	allmenues = []

	for menu in allcategoroies:
		catid = menu.id
		for s in Subcategory.objects.filter(cat_id=int(menu.id)):
			
			allmenues.append({'menuid':s.cat_id , 'submenu_id' : s.id, "submenu_name":s.subcat_name})

		menulist.append({"mainmenu_id":menu.id, "mainmenu_name":menu.cat_name, "submenus":allmenues})
		allmenues= []	


	for c in categoroies:
		cname = c.cat_name
		catimg = c.catimage
		catlist.append({ 
			'catid':c.id,
			'name':cname,
			'image': catimg,
			})

	data = {
	"title":sitesettings[0].site_title,
	"phone":sitesettings[0].site_phone,
	"email":sitesettings[0].site_email,
	"logo":sitesettings[0].site_logo,
	"copyrights":sitesettings[0].copyright,
	'sliders':Sliders.objects.filter(status=1),
	"newprodects": newprodects,
	'catdisplay'       : catlist,
	'todaydeals':todaydeals,
	"bestseller":bestseller,
	"featuredproducts":featuredproducts,
	"menulist":menulist,
	"categoryDisplaylist":categoryDisplaylist,
	"specialofferProdects" : sp,
	'bloddata':bloddata,
	
	}
	
	return render(request, 'aboutus.html', data)

def wihslist(request):
	allwishlist = wishlist.objects.filter(userid=request.user.id)
	prodcts_wishslit = []
	for ap  in allwishlist:
		p  = Prodects.objects.filter(id = ap.prodectid)
		if p.count():
			prodcts_wishslit.append({'id':ap.id, 'wish':p[0]})

	
	sitesettings = Sitesettings.objects.all()
	newprodects = Prodects.objects.filter(position = 'new',state=1)
	categoroies =  Category.objects.order_by('-id')[:5]
	todaydeals = Prodects.objects.filter(position = 'todaydeals',state=1).order_by('-id')[:12]
	bestseller = Prodects.objects.filter(position = 'bestseller',state=1).order_by('-id')[:5]
	featuredproducts = Prodects.objects.filter(position = 'featuredproducts',state=1).order_by('-id')[:5]
	allcategoroies =  Category.objects.all()
	categoryDisplaylist = categoryDisplay.objects.all().order_by("position")
	bloddata = BlogModel.objects.all()
	sp = specialofferProdects.objects.all()
	

	catlist = []
	menulist =[]
	allmenues = []

	for menu in allcategoroies:
		catid = menu.id
		for s in Subcategory.objects.filter(cat_id=int(menu.id)):
			
			allmenues.append({'menuid':s.cat_id , 'submenu_id' : s.id, "submenu_name":s.subcat_name})

		menulist.append({"mainmenu_id":menu.id, "mainmenu_name":menu.cat_name, "submenus":allmenues})
		allmenues= []	


	for c in categoroies:
		cname = c.cat_name
		catimg = c.catimage
		catlist.append({ 
			'catid':c.id,
			'name':cname,
			'image': catimg,
			})

	data = {
	"title":sitesettings[0].site_title,
	"phone":sitesettings[0].site_phone,
	"email":sitesettings[0].site_email,
	"logo":sitesettings[0].site_logo,
	"copyrights":sitesettings[0].copyright,
	'sliders':Sliders.objects.filter(status=1),
	"newprodects": newprodects,
	'catdisplay'       : catlist,
	'todaydeals':todaydeals,
	"bestseller":bestseller,
	"featuredproducts":featuredproducts,
	"menulist":menulist,
	"categoryDisplaylist":categoryDisplaylist,
	"specialofferProdects" : sp,
	'bloddata':bloddata,
	'uid':request.user.id,
	"userwishlist":prodcts_wishslit
	
	}
	return render(request, 'wishlist.html', data)

@login_required(login_url="/login")
def addwishlist(request):
	wishlist(userid=request.user.id, prodectid=request.GET.get('prodectid', '')).save()


@login_required(login_url="/login")
def removewishlist(request):
	rmid = request.GET.get('id', '')
	wishlist.objects.get(id=rmid).delete()
	return redirect("/wihslist")


def blogview(request):

	request.session.modified = True
	sitesettings = Sitesettings.objects.all()
	newprodects = Prodects.objects.filter(position = 'new',state=1)
	categoroies =  Category.objects.order_by('-id')[:5]
	todaydeals = Prodects.objects.filter(position = 'todaydeals',state=1).order_by('-id')[:12]
	bestseller = Prodects.objects.filter(position = 'bestseller',state=1).order_by('-id')[:5]
	featuredproducts = Prodects.objects.filter(position = 'featuredproducts',state=1).order_by('-id')[:5]
	allcategoroies =  Category.objects.all()
	categoryDisplaylist = categoryDisplay.objects.all().order_by("position")
	bloddata = BlogModel.objects.filter(id=request.GET.get("bid", '')).first()
	sp = specialofferProdects.objects.all()
	

	catlist = []
	menulist =[]
	allmenues = []
	for menu in allcategoroies:
		catid = menu.id
		for s in Subcategory.objects.filter(cat_id=int(menu.id)):
			
			allmenues.append({'menuid':s.cat_id , 'submenu_id' : s.id, "submenu_name":s.subcat_name})

		menulist.append({"mainmenu_id":menu.id, "mainmenu_name":menu.cat_name, "submenus":allmenues})
		allmenues= []	


	for c in categoroies:
		cname = c.cat_name
		catimg = c.catimage
		catlist.append({ 
			'catid':c.id,
			'name':cname,
			'image': catimg,
			})
	redirect_to = request.GET.get('next', None)
	if(redirect_to):
		redirect_path= "/login/?next="+redirect_to
	else:
		redirect_path= '/login/'


	users = {}
	data = {"redirect_path":redirect_path,
	"title":sitesettings[0].site_title,
	"phone":sitesettings[0].site_phone,
	"email":sitesettings[0].site_email,
	"logo":sitesettings[0].site_logo,
	"copyrights":sitesettings[0].copyright,
	'sliders':Sliders.objects.filter(status=1),
	"newprodects": newprodects,
	'catdisplay'       : catlist,
	'todaydeals':todaydeals,
	"bestseller":bestseller,
	"featuredproducts":featuredproducts,
	"menulist":menulist,
	"categoryDisplaylist":categoryDisplaylist,
	"specialofferProdects" : sp,
	'bloddata':bloddata,
	
	}
	return render(request, 'blogview.html', data)



def getShippingPrice(request):
	clientcode= request.GET.get("zipcode", False)
	price = 0;
	if(clientcode):
		allzipcodes = zipcodes.objects.filter(zipcode= clientcode);
		if(allzipcodes.count()):
			price = allzipcodes[0].shipingPrice
	return HttpResponse(price);

def getcheckout(request):
	zipcodestate = "Zip code Not selected"
	sprice =0;	 
	cart = request.session.get(settings.CART_SESSION_ID)
	subtotal = 0
	for key, value in cart.items():
		st = int(cart[key]['quantity'])*int(cart[key]['price'])+subtotal
		subtotal = st+subtotal
	zipcodestate=""
	sprice=0
	if request.GET.get("zipcode", False):		
		allzipcodes = zipcodes.objects.filter(zipcode= request.GET.get("zipcode", False));
		if allzipcodes:
			sprice = 0 #allzipcodes[0].shipingPrice
			zipcodestate=""
		else:
			zipcodestate=""
			#zipcodestate="<span style='color:red'>Shiping not available at <b><u>"+request.GET.get("zipcode", False)+"</u></b>   Location</span>"
	else:
		#zipcodestate = "<span style='color:red'>Zip code not selected</span>"
		zipcodestate = ""
	if sprice >0 :
		shippingpricestate = True
	else:
		shippingpricestate = True


	totalprice = subtotal+sprice
	data = {
	"zipcodestate":zipcodestate,
	"sprice":sprice,
	"subtotal":subtotal,
	 "totalprice":totalprice,
	 "totalPriceInpaisa":totalprice*100,
	 "shippingpricestate": shippingpricestate,
	 "fname":request.GET.get('fname',''),
	 "lasttname":request.GET.get('lasttname',''),
	 "phone":request.GET.get('phone',''),
	 "email":request.GET.get('email',''),
	 "flat":request.GET.get('flat',''),
	 "address":request.GET.get('address',''),
	 'city':request.GET.get('city',''),
	 "state":request.GET.get('state',''),
	 "zipcode":request.GET.get('zipcode','')
	}
	request.session['orderdata'] = data
	return render(request, 'checkoutdata.html', data)
	#return HttpResponse(price);

def enquiryProdects(request):
	orderid = str(request.user.id)+str(uuid.uuid1())[:5]
	cart = request.session.get(settings.CART_SESSION_ID)
	subtotal = 0
	for key, value in cart.items():
		st = int(cart[key]['quantity'])*int(cart[key]['price'])+subtotal
		subtotal = st+subtotal

	shippingAddrasString = request.GET.get("fname", '')+"**"+request.GET.get("lasttname", '')+"**"+request.GET.get("email", '')+"**"+request.GET.get("phone", '')+"**"+request.GET.get("flat", '')+"**"+request.GET.get("address", '')+"**"+request.GET.get("city", '')+"**"+request.GET.get("state", '')+"**"+request.GET.get("zip", '')+"**"+request.GET.get("zipcode", '')
	orders(userId  = request.user.id, username=request.GET.get("fname", '')+"__"+request.GET.get("lasttname", ''), 
		phone =   request.GET.get("phone", ''), 
		email = request.GET.get("email", ''), 
		orderId = orderid,
		totalPrice = subtotal,
		subtotalPrice = subtotal,
		shippingprice  = 0,
		orderDate   = date.today(),
		develiveryDate =date.today()+timedelta(days=10) ,
		shippingAddras = shippingAddrasString,
		orderState  = 1,
		odertype = 0
		).save()
	for key, value in cart.items():
		#totalPrice = int(cart[key]['quantity'])*int(cart[key]['price'])
		orderProdects(userId =request.user.id,
			orderId = orderid ,
			prodectId =cart[key]['product_id'],
			prodectName =cart[key]['name'] ,
			prodectPrice =cart[key]['price'] ,
			prodectImage  =cart[key]['image'] ,
			quantity =cart[key]['quantity']).save();
	#print(request.GET)
	return HttpResponse(request.GET);

def gallery(request):
	sitesettings = Sitesettings.objects.all()
	newprodects = Prodects.objects.filter(position = 'new',state=1)
	categoroies =  Category.objects.order_by('-id')[:5]
	todaydeals = Prodects.objects.filter(position = 'todaydeals',state=1).order_by('-id')[:12]
	bestseller = Prodects.objects.filter(position = 'bestseller',state=1).order_by('-id')[:5]
	featuredproducts = Prodects.objects.filter(position = 'featuredproducts',state=1).order_by('-id')[:5]
	allcategoroies =  Category.objects.all()
	categoryDisplaylist = categoryDisplay.objects.all().order_by("position")
	bloddata = BlogModel.objects.all()
	sp = specialofferProdects.objects.all()
	gal  = gallerymodel.objects.all()
	

	catlist = []
	menulist =[]
	allmenues = []

	for menu in allcategoroies:
		catid = menu.id
		for s in Subcategory.objects.filter(cat_id=int(menu.id)):
			
			allmenues.append({'menuid':s.cat_id , 'submenu_id' : s.id, "submenu_name":s.subcat_name})

		menulist.append({"mainmenu_id":menu.id, "mainmenu_name":menu.cat_name, "submenus":allmenues})
		allmenues= []	


	for c in categoroies:
		cname = c.cat_name
		catimg = c.catimage
		catlist.append({ 
			'catid':c.id,
			'name':cname,
			'image': catimg,
			})

	data = {
	"title": sitesettings[0].site_title,
	"phone":sitesettings[0].site_phone,
	"email":sitesettings[0].site_email,
	"logo":sitesettings[0].site_logo,
	"copyrights":sitesettings[0].copyright,
	'sliders':Sliders.objects.filter(status=1),
	"newprodects": newprodects,
	'catdisplay'       : catlist,
	'todaydeals':todaydeals,
	"bestseller":bestseller,
	"featuredproducts":featuredproducts,
	"menulist":menulist,
	"categoryDisplaylist":categoryDisplaylist,
	"specialofferProdects" : sp,
	'bloddata':bloddata,
	"galleryimages":gal
	
	}
	return render(request, 'gallery.html', data)
