from django.shortcuts import render,redirect
from .models import *
from .form import orderForm,CreateUserForm,CustomerForm
from .filters import orderFilters
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unautenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
@unautenticated_user
def registerpage(request):
    form=CreateUserForm()
    if request.method=="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')

            messages.success(request,'Account was Created' + username)
            return redirect('login')
    content={'form':form}
    return render(request,'register.html',content)
@unautenticated_user
def loginpage(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username or password is incorrect')

    content={}
    return render(request,'login.html',content)
def logoutpage(request):
    logout(request)
    return redirect('login')
@login_required(login_url='login')
@admin_only
def home(request):
    customer=Customer.objects.all()
    orders=Order.objects.all()
    total_customer=customer.count()
    total_order=orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='pending').count()
    content={'customer':customer,'orders':orders,'total_order':total_order,'delivered':delivered,'pending':pending}
    return render(request,'dashboard.html',content)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userpage(request):
    orders=request.user.customer.order_set.all()
    total_order = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='pending').count()
    content = {'orders':orders,'total_order':total_order,'delivered':delivered,'pending':pending}
    return render(request, 'user.html', content)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSetting(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)
    if request.method=='POST':
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'account_setting.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()

    return render(request,'product.html',{'product':products})
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request,pk):
    customers = Customer.objects.get(id=pk)
    orders=customers.order_set.all()
    orders_count=orders.count()
    myfilter=orderFilters(request.GET,queryset=orders)
    orders=myfilter.qs
    conent={'customer':customers,'order':orders,'order_count':orders_count,'myfilter':myfilter}
    return render(request,'customer.html',conent)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_Order(request,pk_test):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk_test)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form': formset}
    return render(request, 'form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk_test):
    order=Order.objects.get(id=pk_test)
    form=orderForm(instance=order)
    if request.method=="POST":
        form=orderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request, 'form.html', context)
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk_test):
    order=Order.objects.get(id=pk_test)
    if request.method=="POST":
        order.delete()
        return redirect('/')
    content={'item':order}
    return render(request,'delete.html',content)