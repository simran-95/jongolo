from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib.auth import login as dj_login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest

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

# def order_status(request):
#     add=Blogger.objects.get(id=pk)
#     user_orders = Order.objects.filter(user=request.user)


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


def vender_sign_in(request):
    if request.method == 'POST':
        user_form = Addvender(request.POST)
        reception_form = AddVenderForm(request.POST, request.FILES)

        if user_form.is_valid() and reception_form.is_valid():
            # Save the user data
            user = user_form.save(commit=False)
            user.user_type = 2
            user.set_password(user.password)
            user.save()

            # Save the vender data with the associated user
            reception = reception_form.save(commit=False)
            reception.user = user
            reception.save()

            return HttpResponse('Sign Up Done Successfully!!')
        else:
            print(user_form.errors)
            print(reception_form.errors)
    else:
        user_form = Addvender()
        reception_form = AddVenderForm()

    mydict = {'userForm': user_form, 'receptionForm': reception_form}
    return render(request, 'vender/register.html', context=mydict)



from django.contrib.auth import update_session_auth_hash

# def value(request):
#     user_orders = Vender.objects.filter(user=request.user)
#     return render(request, 'vender/profile.html',{'user_orders':user_orders})

def profile(request):
    user_orders = Vender.objects.filter(user=request.user)
    user_profile = Vender.objects.get(user=request.user)


    if request.method == 'POST':
        fm = Addvender(request.POST, request.FILES, instance=request.user)
        form = AddVenderForm(request.POST, request.FILES, instance=user_profile)
       
        if form.is_valid() and fm.is_valid():
            password = fm.cleaned_data.get('password')
            if password:
                request.user.set_password(password)
                update_session_auth_hash(request, request.user)
            form.save()
            fm.save()

            return redirect('profile')  # Redirect to the user's profile page after successful update
    else:
        form = AddVenderForm(instance=user_profile)
        fm = Addvender(instance=request.user)

    return render(request, 'vender/profile.html', {'form': form, 'fm':fm, 'user_orders':user_orders})


