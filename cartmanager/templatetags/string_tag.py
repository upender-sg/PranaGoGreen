from django import template
from django.utils.safestring import mark_safe

register = template.Library()

#@register.filter()
def imagefilter(imagedata, prodectid):
	images_list =[]
	for img in imagedata,split(","):
		images = {"imagename": img, "prodectid":prodectid}
		images_list.append(images)	
	return images_list


register.filter('imagefilter', imagefilter)
