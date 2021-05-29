"""pranagogreen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from usermanager import views as userviews
from cartmanager import views as cartviews
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', userviews.login,name="login"),
    path('logout/', userviews.logout_view,name="logout"),
    path('dashboard/', include("prodectmanager.urls") , name="dashboard"),
    path('prodects/', cartviews.allprodects , name="allprodects"),
    path('allprodects/', cartviews.allprodects, name="allprodects"),
    path('', include("cartmanager.urls") , name="pranacart"),
    path('cart_add/<int:id>/',cartviews.cart_add , name="cart_add"),
    path('cart_addmulty/',cartviews.cart_add_multy , name="cart_add"),

    path('cart_clear/', cartviews.cart_clear, name='cart_clear'),
    path('itemclear/<int:id>', cartviews.item_clear,  name='itemclear'),
    path('item_decrement/', cartviews.item_decrement,  name='item_decrement'),
    path('itemincrement/', cartviews.itemincrement,  name='item_increment'),
    path('cartdetail/',cartviews.cart_detail,name='cart_detail'),
    path('checkout/',cartviews.checkout,name='checkout'),
    path('sucess/',cartviews.pamentSucess,name='pamentSucess'),
    path('payment/',cartviews.payment,name='payment'),
    path('singleprodect/',cartviews.productsingle,name='productsingle'),
    path('blog/',cartviews.blog,name='blog'),
    path('blogview/',cartviews.blogview,name='blogview'),
    path('signup/', userviews.usersignup, name='usersignup'), 
    path('editprofile/', userviews.editprofile),
    path('profile/', userviews.profile),   
    path('updatecart/', cartviews.updatecart),
    path('contact/', cartviews.contact),
     path('aboutus/', cartviews.aboutus),
    path('wihslist/', cartviews.wihslist),
    path('addwihslist/', cartviews.addwishlist),
    path('removewishlist/', cartviews.removewishlist),
    path('shipping/', userviews.shipping),
     path('zipcodesAjax/', userviews.zipcodesAjax),
     path('myorders/', userviews.myorders),
    path('orderdetails/', userviews.orderdetails),
    path('searchprodect/', userviews.searchprodect),
     path('getShippingPrice/', cartviews.getShippingPrice),
    path('getcheckout/', cartviews.getcheckout),
    path('prodectnquiry/', cartviews.enquiryProdects),
    path('gallery/', cartviews.gallery),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
