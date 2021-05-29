from django.db import models
from django.contrib.auth.models import AbstractBaseUser,User,BaseUserManager, PermissionsMixin
from django.utils import timezone

class UserManager(BaseUserManager):
	use_in_migrations = True
	def create_user(self, fullname, mobile, password, is_active=True, is_staff=True, is_admin=False):
		if not mobile:
			raise ValueError('Mobile Number is required')
		if not password:
			raise ValueError('password is required')

		user_obj = self.model(fullname=fullname, mobile=mobile, password=password)
		user_obj.set_password(password)
		user_obj.admin	= is_admin
		user_obj.staff   = is_staff
		user_obj.active  = is_active

		user_obj.save(using=self._db)
		return user_obj

	def create_staffuser(self, fullname, mobile, password=None):
		user = self.create_user(fullname, mobile, password,is_staff=True,is_admin=False)
		return user

	def create_superuser(self, fullname, mobile, password):
		user = self.create_user(fullname, mobile, password, is_staff=True,is_admin=True)
		return user

class User(AbstractBaseUser,PermissionsMixin):
	
	fullname   	= models.CharField(max_length=100, help_text='fullname is required',error_messages={'unique':'Please enter fullname'})
	lasttname = models.CharField(max_length=100, help_text='first is required',error_messages={'unique':'Please enter firstname'})
	
	mobile     	= models.CharField(max_length=50,unique=True, help_text='mobile number is required',error_messages={'unique':'Please enter mobile number'})
	email     	= models.CharField(max_length=50,null=True, blank=True, help_text='email is required',error_messages={'unique':'Please enter email'}, default="-- --")
	roleId     	= models.PositiveIntegerField(null=True, blank=True)
	role_name   = models.CharField(max_length=50,  null=True, blank=True)
	staff      	= models.BooleanField(default=True)
	admin      	= models.BooleanField(default=False)
	active     	= models.BooleanField(default=False)
	is_hadmin 	= models.BooleanField('hadmin status', default=False)
	is_sadmin 	= models.BooleanField('sadmin status', default=False)
	show_pwd    = models.CharField(max_length=100,  null=True, blank=True)
	is_active = models.BooleanField('Is active', default=True)
	
	date_joined = models.DateTimeField('date joined', default=timezone.now)
	last_logout = models.DateTimeField(null=True)

	objects = UserManager()

	USERNAME_FIELD = 'mobile'
	REQUIRED_FIELDS=['fullname']

	def __str__(self):
		return self.fullname

	def get_fullname(self):
		return self.fullname

	def get_mobile(self):
		return self.mobile

	@property
	def is_superuser(self):
		return self.admin

	@property
	def is_staff(self):
		return self.staff

	@property
	def is_active(self):
		return self.active

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perm(self, app_label):
		return True

class Meta:
	verbose_name = 'user'
	verbose_name_plural = 'users'
	swappable = "AUTH_USER_MODEL"




class shippingaddress(models.Model):
	userid 	= models.PositiveIntegerField(null=True, blank=True)
	flat    = models.CharField(max_length=100,  null=True, blank=True)
	address = models.CharField(max_length=100,  null=True, blank=True)
	city = models.CharField(max_length=100,  null=True, blank=True)
	state  = models.CharField(max_length=100,  null=True, blank=True)
	zipcode = models.CharField(max_length=100,  null=True, blank=True)


class zipcodes(models.Model):
	zipcode = models.CharField(max_length=100,  null=True, blank=True)
	city = models.CharField(max_length=100,  null=True, blank=True)
	shipingPrice= models.PositiveIntegerField(null=True, blank=True)




