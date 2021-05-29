from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import logout as auth_logout, authenticate, login as auth_login
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from usermanager.models import UserManager, zipcodes
from django.contrib import messages
import json


# Create your views here.
from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponseRedirect 
from usermanager import models 
from . import  serializers
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from . models import User, shippingaddress
from prodectmanager.models  import Category, Subcategory,BlogModel, orders, orderProdects,  Prodects,categoryDisplay,Sitesettings, Sliders, specialofferProdects
from cart.cart import Cart
from django.conf import settings
import razorpay
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail



 
def login(request):	
	sitesettings = Sitesettings.objects.all()
	newprodects = Prodects.objects.filter(position = 'new')
	categoroies =  Category.objects.order_by('-id')[:5]
	todaydeals = Prodects.objects.filter(position = 'todaydeals').order_by('-id')[:12]
	bestseller = Prodects.objects.filter(position = 'bestseller').order_by('-id')[:5]
	featuredproducts = Prodects.objects.filter(position = 'featuredproducts').order_by('-id')[:5]
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

	if request.method == "POST":       
		username = request.POST.get('username', "")
		password = request.POST.get('password', "")
		users=authenticate(mobile=request.POST['username'],password=request.POST['password'])
		if users is None:
			messages.error(request,'username or password not correct')
			return render(request, "login.html",  data)
		else:
			if users is not None:
				auth_login(request, users)
				if users.admin == 1 or users.is_sadmin ==1 :					
					return HttpResponseRedirect('/')
				else :
					redirect_to = request.GET.get('next', '/')				
					return HttpResponseRedirect(redirect_to)
			else :
				print("not user ...")
			#return redirect( "/dashboard")

	

	 
	
	return render(request, "login.html",  data)

 
def logout_view(request):
    auth_logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url="/login")
def activate_vender(request):
	if  request.GET.get("venderid", ''):
		mailid = request.GET.get("email", '')
		if request.GET.get("changestate", '')=="deacticate":
			state = 0
			try:
				
				send_mail( 'Aeactivated Activaion', 'Your account has been deactivated. Please contact your site administrator!', 'info@pranagogreen.com',[mailid, "info@pranagogreen.com"])

			except:
				print("Mail Not sent")
  
		else :
			state=1
			try:
				
				send_mail( 'Aeactivated Activaion', 'Your account has been deactivated. Please contact your site administrator!', 'info@pranagogreen.com',[mailid, "info@pranagogreen.com"])

			except:
				print("Mail Not sent")

		phone = User.objects.filter(id=request.GET.get("venderid", '')).update(active=state)

		return HttpResponse("Activated")
	else:
		return HttpResponse("NotActivated")

		

@login_required(login_url="/login")
def profile(request):
	if request.method == "POST":
		phone = User.objects.filter(id=request.user.id)		
		if phone:
			if request.POST.get('mobile', False) and  request.POST.get('fullname', False):
				phone.update(fullname=request.POST.get('fullname'),lasttname=request.POST.get('lasname'), mobile=request.POST.get('mobile'), email=request.POST.get('email'))

	sitesettings = Sitesettings.objects.all()
	newprodects = Prodects.objects.filter(position = 'new')
	categoroies =  Category.objects.order_by('-id')[:5]
	todaydeals = Prodects.objects.filter(position = 'todaydeals').order_by('-id')[:12]
	bestseller = Prodects.objects.filter(position = 'bestseller').order_by('-id')[:5]
	featuredproducts = Prodects.objects.filter(position = 'featuredproducts').order_by('-id')[:5]
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
	"userdata":User.objects.get(id=request.user.id),
	"addrasses": shippingaddress.objects.filter(userid=request.user.id).first()
	
	}

	

	#data= {"userdata":User.objects.filter(id=request.user.id)}
	return render(request, "userdashboard.html", data)
def editprofile(request):
	if request.method == "POST":
		phone = User.objects.filter(id=request.user.id)		
		if phone:
			if request.POST.get('mobile', False) and  request.POST.get('fullname', False):
				phone.update(fullname=request.POST.get('fullname'),lasttname=request.POST.get('lasname'), mobile=request.POST.get('mobile'), email=request.POST.get('email'))
				return HttpResponseRedirect('/profile')
				

	sitesettings = Sitesettings.objects.all()
	newprodects = Prodects.objects.filter(position = 'new')
	categoroies =  Category.objects.order_by('-id')[:5]
	todaydeals = Prodects.objects.filter(position = 'todaydeals').order_by('-id')[:12]
	bestseller = Prodects.objects.filter(position = 'bestseller').order_by('-id')[:5]
	featuredproducts = Prodects.objects.filter(position = 'featuredproducts').order_by('-id')[:5]
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
	"userdata":User.objects.get(id=request.user.id),
	"addrasses": shippingaddress.objects.filter(userid=request.user.id).first()
	
	}

	

	#data= {"userdata":User.objects.filter(id=request.user.id)}
	return render(request, "profile-edit.html", data)

def usersignup(request):
	data = {}
	if request.method == 'POST':
		fname = request.POST.get("fname", '').strip()
		username = request.POST.get("mobile", '').strip()
		password = request.POST.get("password", '').strip()
		eiail = request.POST.get("email",'')
		if User.objects.filter(mobile=username).exists():
			messages.error(request,'PhoneNumeber  is  exists')
			return HttpResponseRedirect('/login')
		if not username and not password:
			return HttpResponseRedirect('/login')
		if request.POST.get('usertype', "") == "user":
			User.objects.create_user(fullname=fname,mobile=username, password=password)
			users = authenticate(mobile=username, password=password)
			User.objects.filter(id=users.id).update(email= eiail)
			try:
				send_mail( 'PranaGoGreen', "User Name:"+ username +  "      Password: "+password, 'info@pranagogreen.com',[eiail, "info@pranagogreen.com"], fail_silently=False,)
				#return HttpResponse(" <b>We've emailed  your password, if an account exists with the email you entered. You should receive them shortly.</b> ")

			except:
				print("Mail Not sent")
			if users is not None:				
				auth_login(request, users)				
				return HttpResponseRedirect('/')
		else:			
			User.objects.create_user(fullname=fname,mobile=username, password=password)
			users = authenticate(mobile=username, password=password)
			User.objects.filter(id=users.id).update(active=0,staff=0, admin=1, email=eiail)
			messages.success(request,'Your account will be placed under review, we will Active your account  with in 24 Hours. If we need more information from you, we will let you know right away.')
			
			return HttpResponseRedirect('/login')
			

	return HttpResponseRedirect('/login')

    

@login_required(login_url="/login")
def shipping(request):
	allzipcodes = zipcodes.objects.all()
	shipingadd = shippingaddress.objects.filter(userid = request.user.id)
	data = {}
	if request.method == "POST":
		if shipingadd.count()>=1 :
			shipingadd.update(flat=request.POST.get('flat', ''),address=request.POST.get('address', ""),
				city=request.POST.get("city", ""),state=request.POST.get('state', ''),zipcode=request.POST.get('zipcode',''))
		else:
			shippingaddress(userid = request.user.id, flat=request.POST.get('flat', ''),address=request.POST.get('address', ""),
				city=request.POST.get("city", ""),state=request.POST.get('state', ''),zipcode=request.POST.get('zipcode','')).save()
		

		pass
		#shipingadd.update()
	return HttpResponseRedirect('/profile')


def zipcodesAjax(request):
	q = request.GET.get('term', '')
	search_qs  = zipcodes.objects.filter(zipcode__startswith=q)
	print(search_qs)
	results = []
	print(q)
	for r in search_qs:
		results.append(r.zipcode)
		data = json.dumps(results)
	mimetype = 'application/json'
	return HttpResponse(data, mimetype)
	
@login_required(login_url="/login")
def  myorders(request):
	data = {}
	allorders = orders.objects.filter(userId = request.user.id)
	allorderProdects = orderProdects.objects.filter(userId = request.user.id).order_by("-id")
	#data = {"alloders":allorders }
	sitesettings = Sitesettings.objects.all()
	newprodects = Prodects.objects.filter(position = 'new')
	categoroies =  Category.objects.order_by('-id')[:5]
	todaydeals = Prodects.objects.filter(position = 'todaydeals').order_by('-id')[:12]
	bestseller = Prodects.objects.filter(position = 'bestseller').order_by('-id')[:5]
	featuredproducts = Prodects.objects.filter(position = 'featuredproducts').order_by('-id')[:5]
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
	"userdata":User.objects.get(id=request.user.id),
	"alloders":allorders,	
	}
 

	return render(request, "myorders.html", data)


@login_required(login_url="/login/?next=myorders")
def orderdetails(request):
	orderId = request.GET.get("orderid")
	allorderProdects = orderProdects.objects.filter(userId = request.user.id, orderId=orderId)
	data = {"prodectdetails":allorderProdects}
	return render(request, 'myordersdetails.html',data)
 
# Redirect to a success page.
#from . import  serializers
#from rest_framework import generics
#from rest_framework.decorators import api_view
#from rest_framework.views import APIView
#from rest_framework.authentication import SessionAuthentication, BasicAuthentication
#from rest_framework.permissions import IsAuthenticated
 
def searchprodect(request):
	search_qs = Prodects.objects.all()
	
	results = []
	data =[];
	for r in search_qs:
		results.append({"name":r.name, "image":r.thumbimg})
	data = json.dumps(results)
	print(data)

	mimetype = 'application/json'
	return HttpResponse(data, mimetype)



def changepassword(request):	
	email=request.GET.get("email", '')
	newpassword = request.GET.get("newpassord", '')
	existemail = User.objects.filter(email=email)
	if existemail:
		from django.contrib.auth import get_user_model
		Userdats = get_user_model().objects.get(email=email)
		if Userdats:
			s= Userdats.set_password(newpassword)			
			Userdats.save();
			try:
				send_mail( 'Password', " Your Password Is: "+newpassword, 'info@pranagogreen.com',[email, "info@pranagogreen.com"], fail_silently=False,)
				return HttpResponse(" <b>We've emailed  your password, if an account exists with the email you entered. You should receive them shortly.</b> ")

			except:
				print("Mail Not sent")
		else :
			return HttpResponse("Email Dose not exist! ")
	else:
		return HttpResponse("<span style='color:red'>Email Dose not exist!</span> ")




def requestpassword(request):
	import secrets
	import string
	N = 5
	res = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(N))
	email=request.GET.get("email", '')
	existemail = User.objects.filter(email=email)
	
	if existemail:		
		from django.contrib.auth import get_user_model
		Userdats = get_user_model().objects.get(email=email)	
		if Userdats:
			#password =  get_user_model().objects.make_random_password()
			s= Userdats.set_password(res)
			
			Userdats.save();
			try:
				send_mail( 'Password', " Your Password Is: "+res, 'info@pranagogreen.com',[email, "info@pranagogreen.com"], fail_silently=False,)
				return HttpResponse(" <b>We've emailed  your password, if an account exists with the email you entered. You should receive them shortly.</b> ")

			except:
				print("Mail Not sent")
		else :
			return HttpResponse("Email Dose not exist! ")
	else:
		return HttpResponse("<span style='color:red'>Email Dose not exist!</span> ")


