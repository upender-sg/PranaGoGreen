from django.db import models
from django.utils.timezone import now

# Create your models here.


class userorders(models.Model):
	orderId = models.CharField(max_lenth=200)
	userId = models.CharField(max_lenth=10)
	created_date = models.DateTimeField(default=now, editable=False)






