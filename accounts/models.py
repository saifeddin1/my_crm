from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
	user 			= models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
	name 			= models.CharField(null=True, max_length=100)	
	phone 			= models.CharField(null=True, max_length=12)
	email 			= models.CharField(null=True, max_length=100)
	date_created 	= models.DateTimeField(null=True, auto_now_add=True)
	profile_pic		= models.ImageField(null=True, blank=True, default='profile.png')	

	def __str__(self):
		return self.name


class Tag(models.Model):
	name 			= models.CharField(null=True, max_length=100)	
	
	def __str__(self):
		return self.name


class Product(models.Model):
	CATEGORY = (
	('Indoor', 'Indoor'),
	('Out Door', 'Out Door'),
	)

	name 			= models.CharField(null=True, max_length=100)	
	price			= models.FloatField(null=True)
	category 		= models.CharField(null=True, max_length=50, choices=CATEGORY)
	description		= models.CharField(null=True, max_length=200, blank=True)
	date_created 	= models.DateTimeField(null=True, auto_now_add=True)
	tags 		    = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name


class Order(models.Model):
	STATUS = (
		('Pending', 'Pending'),
		('Out for delivery','Out for delivery'),
		('Delivered', 'Delivered'),
		)

	customer 		= models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	product 		= models.ForeignKey(Product,  on_delete=models.SET_NULL, null=True)
	date_created 	= models.DateTimeField(null=True, auto_now_add=True)
	status 			= models.CharField(max_length=200, null=True, choices=STATUS)

	def __str__(self):
		return self.product.name
