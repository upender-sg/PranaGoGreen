from django.shortcuts import render, redirect
from django.conf.urls import handler404, handler500, handler403, handler400
from django.http import HttpResponse,JsonResponse
from .models  import Category, Subcategory, Prodects, Sitesettings, gallery, BlogModel, Sliders,specialofferProdects,  homepageProdects, categoryDisplay, orders, orderProdects
from usermanager.models import zipcodes
from django.contrib.auth.decorators import login_required 
from django.core.files.storage import FileSystemStorage
import datetime
import time as dtime
from usermanager.models import User
from PIL import Image  
# Create your views here.
from django import template
register = template.Library()


# Create your views here.


@login_required(login_url="/login/?next=dashboard")
def home(request):

	if   request.user.is_sadmin == 0  and   request.user.admin == 0:
		return redirect('/')
	allprodects = Prodects.objects.all().count()
	allvendors = User.objects.filter(admin=1).count()

	data = {"d":"" , "allprodects":allprodects, "allvendors":allvendors}
	return render(request, "admin/dashboard.html",  data)

#return HttpResponse("request.POST")
@login_required(login_url="/login/?next=dashboard")
def homepagesettings(request):
	if   request.user.is_sadmin == 0  and   request.user.admin == 0:
		return redirect('/')

	Categories = Category.objects.all()
	categoryDisplaylist = categoryDisplay.objects.all().order_by("position")
	sp = specialofferProdects.objects.all();
	todaydeals = Prodects.objects.filter(position='todaydeals');
	allprodects = Prodects.objects.all();
	data = {"allprodects":allprodects,"Categories":Categories, "todaydeals":todaydeals,"categoryDisplaylist": categoryDisplaylist, "soffp":sp}

	return render(request, "admin/homepage_settings.html",  data)


@login_required(login_url="/login/?next=dashboard")
def allprodectbycatsubcat(request):
	
	prodectsByCats = Prodects.objects.filter(cat_id=request.POST['catid'],subcat_id= request.POST['subcatid']).order_by("-id")
	
	data = {"prodectsByCats":prodectsByCats}
	return render(request, "admin/prodects_cats_ajax.html",  data)


@login_required(login_url="/login/?next=dashboard")
def allprodectbycatsubcathomefilter(request):
	prodectsByCats = Prodects.objects.filter(cat_id=request.POST['catid'],subcat_id= request.POST['subcatid']).exclude( position="new").exclude( position="featuredproducts").exclude(position="bestseller").order_by("-id")
	
	data = {"prodectsByCats":prodectsByCats}
	return render(request, "admin/prodects_cats_homefilter_ajax.html",  data)

#think in english... motivate ....basic words....13  tens  , flazes,  
@login_required(login_url="/login/?next=dashboard")
def categorydesplay(request):
	 
	if request.method == "POST":
		for f in request.FILES.getlist("image"):
			milliseconds =int(dtime.time()*1000.0)
			imagename = str(milliseconds)
			x = f			
			categoryDisplay.objects.filter(id=request.POST['catid']).update(cat_id=request.POST['category'],cat_name=request.POST['catname'],image='static/upload/categories/'+imagename+"_"+ str(x)) 
			with open('static_files/upload/categories/'+imagename+"_"+ str(x), 'wb+') as destination:
				for chunk in f.chunks():
					 
					destination.write(chunk)
	return redirect('/dashboard/homesettings')
@login_required(login_url="/login/?next=dashboard")
def specialoffer(request):
	if request.method== "POST":

		s= specialofferProdects.objects.filter(id=1)
		milliseconds =int(dtime.time()*1000.0)
		imagename = str(milliseconds)
		
		for f in request.FILES.getlist("image"):
			x = f
			with open('static_files/upload/sliderimages/'+imagename+"_"+ str(x), 'wb+') as destination:
					for chunk in f.chunks():
						destination.write(chunk)
			s.update(prodectid  = request.POST['prodect'],prodect_name  = request.POST['spprodect_name'], image='static/upload/sliderimages/'+imagename+"_"+ str(x), text=request.POST['txtEditor']);
 
		

	return redirect('/dashboard/homesettings')

	#SPECIAL OFFER

@login_required(login_url="/login/?next=dashboard")
def prodects_alltodaydeals_ajax(request):
	prodectsByCats = Prodects.objects.all().exclude( position="new").exclude( position="featuredproducts").exclude(position="bestseller").order_by("-id")
	
	data = {"prodectsByCats":prodectsByCats}
	return render(request, "admin/prodects_cats_homefilter_ajax.html",  data)

@login_required(login_url="/login/?next=dashboard")
def slider(request):
	if request.method == "POST":
		allimages = '';
		milliseconds =int(dtime.time()*1000.0)
		imagename = str(milliseconds)
		for f in request.FILES.getlist("slider"):
				#def process(f):
				x = f
				with open('static_files/upload/sliderimages/'+imagename+"_"+ str(x), 'wb+') as destination:
					for chunk in f.chunks():
						destination.write(chunk)
					#allimages +='static/upload/sliderimages/'+imagename+"_"+ str(x)+', '; 
		s = Sliders(title=request.POST['slidetitle'],  images = '/static/upload/sliderimages/'+imagename+"_"+ str(x))
		s.save()
	

	sliders = Sliders.objects.all()
	data = {"sliders":sliders}
	return render(request, "admin/sliders.html",  data)

@login_required(login_url="/login/?next=dashboard")
def slidestatus(request):
	if request.POST['slidestate'] == 'off':
		r = Sliders.objects.filter(id=request.POST['slideid'])
		r.update(status=1)
		
	else:
		r = Sliders.objects.filter(id=request.POST['slideid'])
		r.update(status=0)
		
	return HttpResponse(r)




@login_required(login_url="/login/?next=dashboard")
def deleteslider(request):
	r = Sliders.objects.filter(pk=request.POST['id'])
	r.delete()
	return HttpResponse(r)

@login_required(login_url="/login/?next=dashboard")
def categories(request):
	Categories = Category.objects.all()
	data = {"Categories":Categories}
	return render(request, "admin/categories.html",  data)

	
@login_required(login_url="/login/?next=dashboard")
def addcategory(request):
	milliseconds =int(dtime.time()*1000.0)
	imagename = str(milliseconds) #str((datetime.datetime.now()).total_seconds() )
	#catimage
	cimg = '';
	for x in request.FILES.getlist("catimage"):
		def process(f):
			with open('static_files/upload/categories/'+imagename+"_"+ str(x), 'wb+') as destination:
				for chunk in f.chunks():
					destination.write(chunk)
				cimg = '/static/upload/categories/'+imagename+"_"+ str(x)
		process(x)
	c = Category(cat_name=request.POST['catname'], lan=1, catimage=cimg)
	c.save()
		
	
	
	return  redirect('/dashboard/categories')





@login_required(login_url="/login/?next=dashboard")
def delcategory(request):
	#Subcategory.objects.filter(cat_id=request.POST['id']).delete()
	r = Category.objects.filter(pk=request.POST['id'])
	r.delete()
	return HttpResponse('del')

@login_required(login_url="/login/?next=dashboard")
def addsubcategory(request):
	c = Subcategory(cat_id= request.POST['catid'] ,cat_name= request.POST['cat_name'],   subcat_name = request.POST['subcatname'] , lan=1)
	c.save()
	return HttpResponse(request.POST)
@login_required(login_url="/login/?next=dashboard")
def deletesubcategory(request):
	c = Subcategory(id= request.POST['id']).delete()
	
	return HttpResponse(request.POST)

@login_required(login_url="/login/?next=dashboard")
def subcategories(request):
	if request.method == "POST":
		if request.POST['subcats_ajaxcall']:			
			SubCategories = Subcategory.objects.filter(cat_id = request.POST['subcats_ajaxcall'])
			data = { "SubCategories":SubCategories}
			return render(request, "admin/subcategories_ajax.html",  data)
	else :
		SubCategories = Subcategory.objects.all()
		Categories    = Category.objects.all()

		data = {"Categories": Categories, "SubCategories":SubCategories}
		return render(request, "admin/subcategories.html",  data)



@login_required(login_url="/login/?next=dashboard")
def prodects(request):
	data = {}
	categories = Category.objects.all();
	subcategries = Subcategory.objects.all();
	prodects = Prodects.objects.filter(addedby=request.user.id).order_by('-id');
	if request.method == 'GET':
		if  request.GET.get('categoryid'):
			prodects = Prodects.objects.filter(cat_id = request.GET['cateid'], addedby=request.user.id)
		if request.GET.get('subcategoryid'):
			prodects = Prodects.objects.filter(subcat_id = request.GET['subcatid'], addedby=request.user.id)

		data = {"categories": categories,"subcategries":subcategries,  "prodects":prodects }
		return render(request, "admin/prodects.html",  data)
		
@login_required(login_url="/login/?next=dashboard")
def addprodect(request):
	addedby = request.user.id
	if  request.user.is_sadmin:
		approved = 1
	else:
		approved =0

	categories = Category.objects.all();
	subcategries = Subcategory.objects.all();
	data = {"categories": categories,"subcategries":subcategries}		
	if request.method == 'POST':
		rfrprice = int(request.POST.get('reference_pricing', 0));
		isilide = request.POST.get('in_slider', "false")
		inslider =  "true" if isilide  else  "false"
		p= Prodects(cat_id  = request.POST['category_id'],
			subcat_id 	=   request.POST['subcategory_id'],
			cat_name    =  request.POST['category_name'],
			subcat_name  =  request.POST['subcategory_name'],
			lan     	=  'en',
			name  		=  request.POST['prodect_title'],
			price 		= request.POST['prodect_price'],
			oldPrice 	=  '', #request.POST['prodect_oldprice'],
			discount    = request.POST['discount'],
			quantity 	= request.POST['prodect_Quantity'],
			sliderdescription = '' ,# request.POST['sliderdescription'],
			description  =  request.POST['description'],			
			productdetails  =  request.POST['productdetails'],
			position     = request.POST['position'],
			preference_pricing   = rfrprice,
			addedby = addedby,
			approved = approved
			 
		);
		p.save()
		
		prodect_id = p.id

		milliseconds =int(dtime.time()*1000.0)
		imagename = str(milliseconds) #str((datetime.datetime.now()).total_seconds() )
		img=0;
		if inslider == "true":
			for x in request.FILES.getlist("sliderimages"):
				def process(f):
					with open('static_files/upload/sliderimages/'+imagename+str(img)+ str('prana.webp'), 'wb+') as destination:
						for chunk in f.chunks():
							destination.write(chunk)
					#imagename += 'static/upload/'+imagename+"_"+ str(x)+", "
					Sliders(title=request.POST['slidertitle'], prodectid=int(prodect_id), prodecturl='/sinleprodect/?id='+str(prodect_id), 
					 images='/static/upload/sliderimages/'+imagename+str(img)+str('prana.webp')).save()
		
				process(x)
				img= img+1
			#Prodects(id=prodect_id).update(slider='yes')
			

		milliseconds =int(dtime.time()*1000.0)
		imagename = str(milliseconds) #str((datetime.datetime.now()).total_seconds() )
		prodectimageslist=''
		prodectthumbimageslist=''
		i =1;
		loop=0
		for x in request.FILES.getlist("prodectimages"):
			f = x
			with open('static_files/upload/prodectimages/'+imagename+str(i)+str('prana.webp'), 'wb+') as destination:
				for chunk in f.chunks():
					destination.write(chunk)
				prodectimageslist += '/static/upload/prodectimages/'+imagename+str(i)+ str('prana.webp')+", "
				#image = Image.open(r'static/upload/prodectimages/'+imagename+"_"+ str(x)) 
				#MAX_SIZE = (200, 160) 
				#image.thumbnail(MAX_SIZE)
				if i == 1:
					prodectthumbimageslist += '/static/upload/prodectimages/'+imagename+str(i)+ str('prana.webp')
				#image.save('static/upload/prodectimages/thumb_'+imagename+"_"+ str(x))
				i = i+1;

		Prodects.objects.filter(id=prodect_id).update(images=prodectimageslist,image=prodectthumbimageslist,  thumbimg=prodectthumbimageslist )
		 
		#return redirect('/dashboard/prodects')

	return render(request, "admin/addprodect.html",  data)


def editProdect(request):
	prodectid = request.GET.get('pid', '')
	categories = Category.objects.all();
	subcategries = Subcategory.objects.all();
	prodects = Prodects.objects.get(id=prodectid);
	subcategorydata = Subcategory.objects.get(id=prodects.subcat_id)
	prodects.subcat_name = subcategorydata.subcat_name
	imagesObj = []
	i =1;
	for im in prodects.images.split(", "):
		if  len(im)>10:
			imagesObj.append({"path":im})
		

	data = {"categories": categories,"subcategries":subcategries,  "prodects":prodects, "allimages":imagesObj }	
	return render(request, "admin/edit_prodect.html",  data)

@login_required(login_url="/login/?next=dashboard")
def deleteProdect(request):
	r = Prodects.objects.get(pk=request.GET['id'])
	r.delete()
	return redirect('/dashboard/prodects')

@login_required(login_url="/login/?next=dashboard")
def prodectedit(request):
	if request.method == "POST":		
		allimages = ''
		thumbimg ='';
		if request.POST.get("totalimages", False):
			allimages +=request.POST.get("totalimages", False)+", "


		prodectid= request.POST.get("prodectid", False)
		if request.FILES.getlist("prodectimages"):
			milliseconds =int(dtime.time()*1000.0)
			imagename = str(milliseconds)
			for f in request.FILES.getlist("prodectimages"):
				x=f
				
				with open('static_files/upload/prodectimages/'+imagename+"_"+ str(x), 'wb+') as destination:
					for chunk in f.chunks():
						destination.write(chunk)

					#Prodects.objects.filter(id=pid).update(position= request.POST['position'])
				if not allimages:
					thumbimg = '/static/upload/prodectimages/'+imagename+"_"+ str(x)
				else :
					thumbimg = Prodects.objects.get(id=prodectid).image
				allimages += '/static/upload/prodectimages/'+imagename+"_"+ str(x)+", "


				
        
		Prodects.objects.filter(id=prodectid).update(
			cat_id=request.POST.get("category_id", ""),
			cat_name=request.POST.get("category_name", ""),
			subcat_id=request.POST.get("subcategory_id", ""),
			subcat_name=request.POST.get("subcategory_name", ""),
			name=request.POST.get("prodect_title", ""),			
			price=request.POST.get("prodect_price", ""),
			oldPrice=request.POST.get("prodect_oldprice", ""),
			discount=request.POST.get("discount", ""),
			description=request.POST.get("description", ""),
			productdetails=request.POST.get("productdetails", ""),
			images=allimages,
			image = thumbimg,			
			position=request.POST.get("position", ""),
			preference_pricing=request.POST.get("reference_pricing", "")
			);
		return redirect("/dashboard/editprodect?pid="+prodectid)
	return redirect("/dashboard/prodects")



@login_required(login_url="/login/?next=dashboard")
def settings(request):
	if request.method == "POST":
		if request.POST['siteTitle']:			
			i = Sitesettings.objects.update(site_title=request.POST['siteTitle'])
			return redirect('/dashboard/settings') 
		
	settings = Sitesettings.objects.all()
	logo =''
	data = {}
	
	if settings.count()>0 :
		logo =settings[0].site_logo

		data = {"siteTitle": settings[0].site_title,
		"siteemail": settings[0].site_email,
		"logo":settings[0].site_logo,
		"sitephone":settings[0].site_phone,
		"siteemail":settings[0].site_email,
		"copyright":settings[0].copyright,
		"referenceprice": settings[0].reference_pricing,


		}
	return render(request, "admin/settings.html",  data)


@login_required(login_url="/login/?next=dashboard")
def sitelogo(request):
	
	if request.method == "POST":
		if request.FILES.getlist("sitelogo"):
			milliseconds =int(dtime.time()*1000.0)
			imagename = str(milliseconds) 
			for f in request.FILES.getlist("sitelogo"):
				#def process(f):
				x=f
				with open('static_files/upload/siteimages/'+imagename+"_"+ str(x), 'wb+') as destination:
					for chunk in f.chunks():
						destination.write(chunk)
				
				i = Sitesettings.objects.update(site_logo='/static/upload/siteimages/'+imagename+"_"+ str(x))
	#return redirect('/dashboard/settings'
	return redirect('/dashboard/settings')


@login_required(login_url="/login/?next=dashboard")
def sitephone(request):
	if request.POST['sitephone']:
			i = Sitesettings.objects.update(site_phone=request.POST['sitephone'])
			return redirect('/dashboard/settings')

@login_required(login_url="/login/?next=dashboard")
def siteemail(request):
	if request.POST['siteemail']:
		i = Sitesettings.objects.update(site_email=request.POST['siteemail'])
		print(request.POST['siteemail'])
		return redirect('/dashboard/settings')

@login_required(login_url="/login/?next=dashboard")
def copyright(request):
	if request.POST['copyright']:
		i = Sitesettings.objects.update(copyright=request.POST['copyright'])
		return redirect('/dashboard/settings')

@login_required(login_url="/login/?next=dashboard")
def referenceprice(request):
	if request.method == "POST":
		#return HttpResponse(request.POST['reference_price'])
		i = Sitesettings.objects.update(reference_pricing=request.POST['reference_price'])
		return redirect('/dashboard/settings')


def blogdata(request):
	if request.method == "POST":
		if request.FILES.getlist("blogimg"):
			milliseconds =int(dtime.time()*1000.0)
			imagename = str(milliseconds) 
			for f in request.FILES.getlist("blogimg"):
				#def process(f):
				x=f
				with open('static_files/upload/siteimages/'+imagename+"_"+ str(x), 'wb+') as destination:
					for chunk in f.chunks():
						destination.write(chunk)				
				BlogModel(blogtitle=request.POST['title'], blogimage='static/upload/siteimages/'+imagename+"_"+ str(x), blogdesc=request.POST['description']).save()

	
	bd =   BlogModel.objects.all();
	data= {"blogdata":bd}
	return render(request, "admin/blog.html",  data)
	

@login_required(login_url="/login/?next=dashboard")
def vendor(request):
	allvendors = User.objects.filter(admin=1)
	data = {'vendors':allvendors}
	return render(request, "admin/vendor.html",  data)



@login_required(login_url="/login/?next=dashboard")
def adminorders(request):
	allorder_spending = orders.objects.filter(odertype=1).order_by('-id')
	allorders = []
	for ap in allorder_spending:
		for l in ap.prodect_addedby.split(", "):
			if l:
				if request.user.id ==int(l):
					allorders.append(ap)	 

	orders_shipped    =  orders.objects.filter(orderState=2)
	data = {
		"pending_orders":allorders,
		"shipped_orders":orders_shipped,
		"allorders":allorders
	}

	return render(request, "admin/adminorders.html",  data)




@login_required(login_url="/login/?next=dashboard")
def zipcode(request):
	if request.method == "POST":
		zipcodes(zipcode=request.POST.get("zipcode", ''),city=request.POST.get("city", ''), shipingPrice=request.POST.get("shippingprice", False)).save()
	allzipcodes = zipcodes.objects.all()

	data= {"zipcodes": allzipcodes}
	return render(request, "admin/zipcodes.html",  data)
def deletezicode(request):
	if request.GET.get('zipid', ''):
		zicodes.objects.get(id=request.GET.get('zipid', '')).delete()
		return redirect('/dashboard/zipcode')


def handler404(request,exception):
	return redirect('/')

def editcat(request):
	succ=Category.objects.filter(id=request.GET.get("catid", "")).update(cat_name=request.GET.get('catname'))

	return HttpResponse(succ)

def editsubcat(request):
	succ=Subcategory.objects.filter(id=request.GET.get('subcatid', '') ).update(subcat_name=request.GET.get('subcatval', ''))
	return HttpResponse(succ)



def userPurcheslist(request):
	userorderlist= User.objects.filter(is_sadmin=0).filter( admin=0)
	data= {'userorderlist':userorderlist}
	return render(request, "admin/userpurches.html",  data)

def changeorderstatus(request):
	orderid = request.GET.get('id', '')
	orderstate = request.GET.get('orderstate', '')
	orders.objects.filter(id=orderid).update(orderState=orderstate)
	return HttpResponse(request.GET.get('id', ''))

def galleryimages(request):
	
	if request.method == "POST":
		for f in request.FILES.getlist("image"):
			milliseconds =int(dtime.time()*1000.0)
			imagename = str(milliseconds)
			x = f
			gallery(image='static/upload/gallery/'+imagename+"_"+ str(x)).save()			
			#categoryDisplay.objects.filter(id=request.POST['catid']).update(cat_id=request.POST['category'],cat_name=request.POST['catname'],image='static/upload/categories/'+imagename+"_"+ str(x)) 
			with open('static_files/upload/gallery/'+imagename+"_"+ str(x), 'wb+') as destination:
				for chunk in f.chunks():					 
					destination.write(chunk)
	allimages = gallery.objects.all();
	data = {'gallery':allimages}

	return render(request, "admin/gallery.html",  data)
def gallerydelete(request):
	allimages = gallery.objects.get(id=request.GET.get('gid', '')).delete();
	return redirect('/dashboard/gallery')
def changeprodectState(request):
	if request.GET.get("prodectid", False):
		Prodects.objects.filter(id=request.GET.get("prodectid", False)).update(state=request.GET.get("state", False))
		return HttpResponse(request.GET.get("state", False))

def vendorprodects(request):
	prodects = Prodects.objects.all().exclude(addedby=request.user.id).order_by('-id');
	data = {  "prodects":prodects }

	return render(request, "admin/vedorprodects.html",  data)


def approvevendorprodects(request):
	if request.GET.get("prodectid", False):
		Prodects.objects.filter(id=request.GET.get("prodectid", False)).update(approved=request.GET.get("state", False))
		return HttpResponse(request.GET.get("state", False))



@login_required(login_url="/login/?next=dashboard")
def vendororders(request):
	allorder_spending = orders.objects.filter(odertype=1).order_by('-id')
	allorders = []
	for ap in allorder_spending:
		for l in ap.prodect_addedby.split(", "):
			if l:
				if request.user.id !=int(l):
					allorders.append(ap)	 

	orders_shipped    =  orders.objects.filter(orderState=2)
	data = {
		"pending_orders":allorders,
		"shipped_orders":orders_shipped,
		"allorders":allorders
	}
	return render(request, "admin/vendorOrders.html",  data)

def orderProdectsview(request):
	orderid = request.GET.get("oid", False)
	prodects = orderProdects.objects.filter(orderId=orderid).order_by('-id')
	data = {}
	data = {}
	categories = Category.objects.all();
	subcategries = Subcategory.objects.all();	 
	data = {"categories": categories,"subcategries":subcategries,  "prodects":prodects }
		
	return render(request, "admin/orderprodectlist.html",  data)