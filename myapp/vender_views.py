from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib.auth import login as dj_login, logout, authenticate
from django.contrib import messages


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_product')
    else:
        form = ProductForm()

    return render(request, 'vender/add_product.html', {'form': form})


def view_product(request):
    user = Product.objects.all()
    return render(request, 'vender/view_product.html',{'user':user})
    

def delete_product(request,id):
    user = Product.objects.get(id=id)
    user.delete()
    return redirect('view_product')


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