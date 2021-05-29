from django.db import models
from datetime import datetime


# Create your models here.

# Create your models here.

class Menu(models.Model):
    menu_name = models.CharField(max_length=100)
    menu_link = models.CharField(max_length=200) 
    lan       =  models.PositiveIntegerField()

class Category(models.Model):
    cat_name = models.CharField(max_length=100)
    lan     =  models.PositiveIntegerField()
    catimage = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
    	return self.cat_name;

class Subcategory(models.Model):
	cat_id		= models.PositiveIntegerField()
	cat_name		= models.CharField(max_length=100)
	subcat_name = models.CharField(max_length=100)
	lan     	=  models.PositiveIntegerField()

	def __str__(self):
		return self.subcat_name





class Prodects(models.Model):
	cat_id 		= models.PositiveIntegerField()
	subcat_id 	= models.PositiveIntegerField()
	cat_name    =  models.CharField(max_length=100)
	subcat_name  =  models.CharField(max_length=100)
	lan     	=  models.CharField(max_length=10, default='')
	name  		=  models.CharField(max_length=100)
	price 		= models.CharField(max_length=100)
	oldPrice 	= models.CharField(max_length=100)
	discount  = models.CharField(max_length=100,blank=True, null=True)
	quantity 	= models.CharField(max_length=100)
	sliderdescription =  models.TextField()
	description =  models.TextField()
	productdetails=  models.TextField()
	images 		= models.TextField(blank=True, null=True)
	image       = models.TextField(blank=True, null=True)
	thumbimg 	=  models.TextField(blank=True, null=True)
	position     = models.CharField(max_length=100,blank=True, null=True)	
	slider    = models.CharField(max_length=100, default='no')	
	preference_pricing   =  models.PositiveIntegerField(default=0)
	sold   =  models.PositiveIntegerField(default=0);
	url  =  models.CharField(max_length=100, default='no')
	addedby = models.CharField(max_length=100, default='no');
	state = models.PositiveIntegerField(default=0);
	approved = models.PositiveIntegerField(default=0);



	def __str__(self):
		return self.name


class Sitesettings(models.Model):
	site_title   = models.CharField(max_length=200, default='no')
	site_phone   = models.CharField(max_length=200, default='no')
	site_email   =  models.CharField(max_length=200, default='no')
	site_logo    =  models.CharField(max_length=200, default='')
	footer_text  =  models.CharField(max_length=200, default='no')
	copyright    = models.CharField(max_length=200, default='no') 
	reference_pricing  = models.PositiveIntegerField(default=0)
	sitestatus   = models.PositiveIntegerField(default=0)     

class homepageProdects(models.Model):
	cat_id 		= models.PositiveIntegerField(default=0)
	subcat_id 	= models.PositiveIntegerField(default=0)
	cat_name    =  models.CharField(max_length=100, default='no')
	subcat_name  =  models.CharField(max_length=100, default='no')
	prodect_id   =  models.CharField(max_length=100, default='no')
	prodect_name =  models.CharField(max_length=200, default='no')
	image = models.CharField(max_length=200, default='no');
	postion_name =  models.CharField(max_length=200, default='no');
	position     = models.PositiveIntegerField(default=0) 

class categoryDisplay(models.Model):
	cat_id 		= models.PositiveIntegerField(default=0)
	cat_name 	= models.CharField(max_length=200, default='no')
	image       = models.CharField(max_length=200, default='no');
	position    = models.PositiveIntegerField(default=1)

class specialofferProdects(models.Model):
	prodectid    = models.PositiveIntegerField(default=0)
	prodect_name  = models.CharField(max_length=200, default='no');
	image        = models.CharField(max_length=200, default='no');
	text         =   models.CharField(max_length=500, default='');

class Sliders(models.Model):
	title           =  models.CharField(max_length=200)
	prodectid     	=  models.PositiveIntegerField(default=0)
	prodecturl 	    =  models.CharField(max_length=200, default='')
	images 	        =  models.TextField(blank=True, null=True)
	pos       		=  models.PositiveIntegerField(default=1)
	status          =  models.PositiveIntegerField(default=0)  

	def __str__(self):
		return self.title

class BlogModel(models.Model):
	blogtitle =   models.CharField(max_length=200, default='')
	blogimage =  models.CharField(max_length=200, default='')
	blogdesc =  models.TextField(default='')
	date = models.DateField(default=datetime.now)


class wishlist(models.Model):
	
	userid = models.PositiveIntegerField(default=0)
	prodectid =  models.PositiveIntegerField(default=0)
	date = models.DateField(default=datetime.now)


class orders(models.Model):
	userId  = models.PositiveIntegerField(default=0)
	username =  models.CharField(max_length=200, default='')
	phone =   models.CharField(max_length=200, default='')
	email =  models.CharField(max_length=200, default='')
	orderId = models.CharField(max_length=200, default='')
	totalPrice =  models.CharField(max_length=200, default='')
	subtotalPrice =  models.CharField(max_length=200, default='')
	shippingprice  =  models.CharField(max_length=200, default='')
	orderDate   =  models.CharField(max_length=50, default='')
	develiveryDate =  models.CharField(max_length=50, default='')
	shippingAddras =  models.TextField(blank=True, null=True)
	orderState  =  models.CharField(max_length=200, default='1')
	odertype = models.CharField(max_length=10, default='1')
	prodect_addedby = models.CharField(max_length=10, default='')
	


class orderProdects(models.Model):
	userId    = models.PositiveIntegerField(default=0)
	orderId   = models.CharField(max_length=200, default='')
	prodectId = models.CharField(max_length=200, default='')
	prodectName = models.CharField(max_length=200, default='') 
	prodectPrice = models.CharField(max_length=200, default='') 
	prodectImage  = models.CharField(max_length=200, default='')
	prodect_addedby = models.CharField(max_length=200, default='')	
	quantity = models.CharField(max_length=10, default='')


	
class gallery(models.Model):
	title= models.CharField(max_length=200, default='')
	image =   models.CharField(max_length=200, default='') 



