from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func): #takes in the view that has this decorator
	def wrapper_func(request, *args, **kwargs): #runs 
		if request.user.is_authenticated: #this code 
			return redirect('home')	# before the actual code in the view
		else: # and then 
			return view_func(request, *args, **kwargs) #run the actual view

	return wrapper_func


def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse('Not allowed !')
			
		return wrapper_func
	return decorator



def admin_only(view_func):
	def wrapper_func(request, *args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == 'customer':
			return redirect('user-page')
		if group == 'admin':
			return view_func(request, *args, **kwargs)

	return wrapper_func






























