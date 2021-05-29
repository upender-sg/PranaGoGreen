from django import template
from prodectmanager.models import  homepageProdects

register = template.Library()



@register.filter(name='split')
def split(value):
	print("***********")
	print(value)



def prodectfilter_postion(value, arg):
	print(value)	

	return value*arg


register.filter('prodectfilter_postion', prodectfilter_postion)
