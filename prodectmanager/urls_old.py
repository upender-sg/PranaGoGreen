from django.contrib import admin
from django.urls import path, include
from . import views
from usermanager import views as userviews
 

urlpatterns = [
    path('', views.home),
	path('prodects', views.prodects),
	path('addprodect', views.addprodect),
	path('editprodect', views.editProdect),
	path('deleteprodect', views.deleteProdect),
	path('subcategories', views.subcategories),
    path('categories', views.categories),
	path('addcategory', views.addcategory),
    path('addsubcategory', views.addsubcategory),
    path('settings', views.settings),
	path('sitelogo', views.sitelogo),
	path('sitephone', views.sitephone),
	path('siteemail', views.siteemail),
	path('copyright', views.copyright),
	path('copyright', views.referenceprice),
	path('delcategory', views.delcategory),
	path('deletesubcategory', views.deletesubcategory),
	path('sliders', views.slider),
	path('deleteslider', views.deleteslider),
	path('slidestatus', views.slidestatus),
	path('homesettings', views.homepagesettings),
	path('allprodectbycatsubcat', views.allprodectbycatsubcat),
	path('prodects_cats_homefilter_ajax', views.allprodectbycatsubcathomefilter),
    path('prodectedit', views.prodectedit),
    path('prodectsalltodaydealsajax', views.prodects_alltodaydeals_ajax),
    path('categorydesplay', views.categorydesplay),
    path('specialoffer', views.specialoffer),
    path('blog', views.blogdata),
    path('vendor', views.vendor),
    path('orders', views.adminorders),
    path('zipcode', views.zipcode),
    path('editcat', views.editcat),
     path('editsubcat', views.editsubcat),
 	path('userPurcheslist', views.userPurcheslist),
	path('changeorderstatus', views.changeorderstatus),
	path('gallery', views.galleryimages),
    path('gallerydelete', views.gallerydelete),
    path('activatevender', userviews.activate_vender),
    



    ]