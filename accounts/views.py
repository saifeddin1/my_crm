from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, Customer
from django.forms import inlineformset_factory
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only



@unauthenticated_user
def registerPage(request):
	form =CreateUserForm()
	if request.method == 'POST':
		form =CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')			
			messages.success(request, 'Account Created For '+ username)
			return redirect('login')

	context = {'form':form}
	return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'username or password is incorrect !')
	context = {}
	return render(request, 'accounts/login.html', context)


def logoutUser(request):
	logout(request)
	return redirect('login')




@login_required(login_url='login')
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customer = customers.count() #counts customers
	total_orders = orders.count() #counts orders

	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'customers': customers,
				'orders':orders,
				'total_customer':total_customer,
				'total_orders':total_orders,
				'delivered':delivered,
				'pending':pending,
	}
	return render(request, 'accounts/dashboard.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	customers = Customer.objects.all()
	orders = request.user.customer.order_set.all()
	total_orders = orders.count() #counts customers
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders,
				'total_orders':total_orders,
				'delivered':delivered,
				'pending':pending,}
	return render(request, 'accounts/user.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer 	= request.user.customer 
	if request.method == 'POST':
		form 	= CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()

	form 	= CustomerForm(instance=customer)
	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()
	context = {'products': products,
	}
	return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk):
	customer = Customer.objects.get(id=pk)
	print(customer.name)
	orders = customer.order_set.all()
	filter_form = OrderFilter(request.GET, queryset=orders)
	orders = filter_form.qs 
	context = {'customer': customer,
				'orders':orders,
				'filter_form':filter_form,
	}
	return render(request, 'accounts/customer.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
	customer = get_object_or_404(Customer, id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
	# form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('../')

	context = {'formset':formset}
	return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
	customer = get_object_or_404(Customer, id=pk)
	instance = get_object_or_404(Order, id=pk)
	formset = OrderFormSet(instance=customer)
	if request.method == 'POST':
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('../')
	context = {'formset':formset}
	return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	instance = get_object_or_404(Order, id=pk)
	instance.delete()
	return redirect('home')

