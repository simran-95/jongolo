from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib.auth import login as dj_login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required (login_url='/')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # Set the user field before saving
            product = form.save(commit=False)
            product.user = request.user  # Set the user to the logged-in user
            product.save()
            return redirect('view_product')
    else:
        form = ProductForm()

    return render(request, 'vender/add_product.html', {'form': form})


@login_required (login_url='/')
def view_product(request):
    user = Product.objects.all()
    return render(request, 'vender/view_product.html',{'user':user})
    

@login_required (login_url='/')
def delete_product(request,id):
    user = Product.objects.get(id=id)
    user.delete()
    return redirect('view_product')

@login_required (login_url='/')
def update_product(request,pk):
    if request.method=="POST":
        pi=Product.objects.get(pk=pk)
        fm=ProductForm(request.POST,request.FILES,instance=pi)
        if fm.is_valid():
            fm.save()
            return redirect('view_product')
    else:
            pi = Product.objects.get(id=pk)
            fm = ProductForm(instance=pi)
            context = {'pi':pi,'fm':fm}
    return render(request,'vender/update_product.html',context)


def earning(request):
    return render(request, 'vender/earning.html')


def order_status(request):
    user_orders = Order.objects.filter(user=request.user)
    return render(request, 'vender/order_vender.html',{'user_orders':user_orders})



# def project_allow(request, id):
#     developer=Team.objects.get(id=id)
#     developer.status = 0
#     developer.save()
#     return redirect('list3')

# def project_completed(request, id):
#     developer=Team.objects.get(id=id)
#     developer.status = 1
#     developer.save()
#     return redirect('list3')

# def project_pending(request, id):
#     developer=Team.objects.get(id=id)
#     developer.status = 2
#     developer.save()
#     return redirect('list3')