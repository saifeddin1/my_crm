from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Customer  
from django.contrib.auth.models import Group


def customer_profile(sender, instance, created, **kwargs):

	'''
		Arguments sent with this signal:
		sender: The model class.
		instance: The actual instance being saved.
		created: A boolean; True if a new record was created.
	'''

	if created:
		group = Group.objects.get(name='customer')
		instance.groups.add(group)
		Customer.objects.create(user=instance,
								 name=instance.username,
								 email=instance.email)

		print('profile created !!!!!')
post_save.connect(customer_profile, sender=User) #sender need to be a class

