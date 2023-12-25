from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth import login as dj_login, logout, authenticate
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

# Create your views here.

# def login(request):
#     return render(request, 'admin-login.html')


@login_required(login_url='/login')
def earning_admin(request):
    user_orders = Order.objects.all()
    user_products = Product.objects.all()
    total_earnings = sum(product.total_earnings() for product in user_products)
    return render(request, 'earning_admin.html',{'user_products':user_products, 'total_earnings':total_earnings, 'user_orders':user_orders})


def superadmin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        user = authenticate(request,
            email=request.POST.get('email'),
            password=request.POST.get('password'),
        )
        if user and user.user_type == User.SUPERUSER:
            dj_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'admin-login.html')


def blogger_login(request):
    if request.method == 'POST':
        user = authenticate(request,
            email=request.POST.get('email'),
            password=request.POST.get('password'),
        )
        if user and user.user_type == User.BLOGGER:
            dj_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'admin-login.html')


def vender_login(request):
    print('..login page opened..')
    if request.method == 'POST':
        user = authenticate(request,
            email=request.POST.get('email'),
            password=request.POST.get('password'),
        )
        if user and user.user_type == User.VENDER:
            dj_login(request, user)
            return redirect('dashboard-add')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'websiteuser/website-login.html')


def doLogin(request):
    if request.method=='POST':
        user=authenticate(request,
            email=request.POST.get('email'),
            password=request.POST.get('password'),)
        if user!=None:
            dj_login(request,user) 
            user_type=user.user_type
       
            # if user_type==User.SUPERUSER:
               
            #    return redirect('dashboard')
           
            # if user_type==User.VENDER:
               
            #     return redirect('dashboard-add')
            if user_type==User.ADDUSER:
               
                return redirect('dashboard-web')
            elif user_type==User.BLOGER:
               
                return redirect('dashboard-blog')
            else:
                messages.error(request,'invalid credentials')
                return redirect('login1')
        else:
            messages.error(request,'invalid credentials')

    return redirect('login1')

    
@login_required(login_url='/login')
def index(request):
    return render(request, 'demo.html')

@login_required(login_url='/login')
def dashboard(request):
    return render(request, 'index.html')

@login_required(login_url='/')
def dashboard1(request):
    return render(request, 'vender/dashboard-add.html')

@login_required(login_url='/')
def dashboard3(request):
    return render(request, 'vender/dashboard-blog.html')
    
def base(request):
    return render(request, 'websiteuser/base.html')


def custom_logout(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='login')
def add_user(request):
    userForm=Adduser()
    receptionForm=AddUserForm()
    mydict={'userForm':userForm,'receptionForm':receptionForm}
    if request.method=='POST':
        userForm=Adduser(request.POST)
        receptionForm=AddUserForm(request.POST, request.FILES)
        if userForm.is_valid() and receptionForm.is_valid():
            user=userForm.save()
            user.user_type=3
            user.set_password(user.password)
            user.save()

            reception=receptionForm.save(commit=False)
            reception.user=user
           
            reception.save()
            return redirect('super_admin/view_user')
        else:
            print(userForm.errors)
            print(receptionForm.errors)
        
    return render(request, 'add_user.html', context=mydict)

@login_required(login_url='/login')
def view_user(request):
    user = AddUser.objects.all()
    return render(request, 'view_user.html',{'user':user})

@login_required(login_url='/login')
def delete_user(request,id):
    u = AddUser.objects.get(id=id)
    u.delete()
    return redirect('super_admin/view_user')

@login_required(login_url='/login')
def update_user(request,pk):
    vender = AddUser.objects.get(id=pk)
    user = vender.user

    if request.method == 'POST':
        userForm = Adduser(request.POST, instance=user, prefix='vender_user')
        adduserForm = AddUserForm(request.POST, request.FILES, instance=vender, prefix='vender1')
        
        if userForm.is_valid() and adduserForm.is_valid():
            password = userForm.cleaned_data.get('password')
            if password:
                user.set_password(password)
                update_session_auth_hash(request, user)
            userForm.save()
            adduserForm.save()
            return redirect('super_admin/view_user')  # Replace 'success_url' with the desired URL
        else:
            print(userForm.errors)
            print(adduserForm.errors)
    else:
        userForm = Adduser(instance=user, prefix='vender_user')
        adduserForm = AddUserForm(instance=vender, prefix='vender1')
    return render(request,'update_user.html',{'adduserForm': adduserForm, 'userForm': userForm})


@login_required(login_url='/login')
def add_vendor(request):
    userForm=Addvender()
    receptionForm=AddVenderForm()
    mydict={'userForm':userForm,'receptionForm':receptionForm}
    if request.method=='POST':
        userForm=Addvender(request.POST)
        receptionForm=AddVenderForm(request.POST, request.FILES)
        if userForm.is_valid() and receptionForm.is_valid():
            user=userForm.save()
            user.user_type=2
            user.set_password(user.password)
            user.save()

            reception=receptionForm.save(commit=False)
            reception.user=user
           
            reception.save()
            return redirect('super_admin/view_vender')
        else:
             print(userForm.errors)
             print(receptionForm.errors)
        
    return render(request, 'add_vender.html', context=mydict)

@login_required(login_url='/login')
def view_vender(request):
    user = Vender.objects.all()
    return render(request, 'view_vender.html',{'user':user})

@login_required(login_url='/login')
def delete_vender(request,id):
    u = Vender.objects.get(id=id)
    u.delete()
    return redirect('super_admin/view_vender')
    

@login_required(login_url='/login')
def update_vender(request,pk):
    
    vender = Vender.objects.get(id=pk)
    user = vender.user

    if request.method == 'POST':
        pharmacist_user_form = Addvender(request.POST, instance=user, prefix='vender_user')
        pharmacist_form = AddVenderForm(request.POST, request.FILES, instance=vender, prefix='vender1')
        
        if pharmacist_user_form.is_valid() and pharmacist_form.is_valid():
            password = pharmacist_user_form.cleaned_data.get('password')
            if password:
                user.set_password(password)
                update_session_auth_hash(request, user)
            pharmacist_user_form.save()
            pharmacist_form.save()
            return redirect('super_admin/view_vender')  # Replace 'success_url' with the desired URL
        else:
            print(pharmacist_user_form.errors)
            print(pharmacist_form.errors)
    else:
        pharmacist_user_form = Addvender(instance=user, prefix='vender_user')
        pharmacist_form = AddVenderForm(instance=vender, prefix='vender1')
    
    return render(request, 'update_vender.html', {'pharmacist_user_form': pharmacist_user_form, 'pharmacist_form': pharmacist_form})

    
@login_required(login_url='/login')
def add_blogger(request):
    userForm = Addblogger()
    bloggerForm = AddBlogerForm()
    mydict = {'userForm': userForm, 'bloggerForm': bloggerForm}

    if request.method == 'POST':
        userForm = Addblogger(request.POST)
        bloggerForm = AddBlogerForm(request.POST, request.FILES)

        if userForm.is_valid() and bloggerForm.is_valid():
            user = userForm.save()
            user.user_type = 4  # Use the string '4' for the 'Blogger' user type
            user.set_password(user.password)
            user.save()

            # Fix the indentation here
            reception = bloggerForm.save(commit=False)
            reception.user = user
            reception.save()

            return redirect('super_admin/view_bloger')
        else:
            print(userForm.errors)
            print(bloggerForm.errors)
            return render(request, 'add_bloger.html', context=mydict)
    
    return render(request, 'add_bloger.html', context=mydict)

@login_required(login_url='/login')
def view_blogger(request):
    user = Blogger.objects.all()
    return render(request, 'view_bloger.html',{'user':user})

@login_required(login_url='/login')
def delete_blogger(request,id):
    u = Blogger.objects.get(id=id)
    u.delete()
    return redirect('super_admin/view_bloger')   

@login_required(login_url='/login')
def update_blogger(request,id):

    vender = get_object_or_404(Blogger, pk=id)

    user = vender.user

    if request.method == 'POST':
        userForm = Addblogger(request.POST, instance=user, prefix='vender_user')
        adduserForm = AddBlogerForm(request.POST, request.FILES, instance=vender, prefix='vender1')

        if userForm.is_valid() and adduserForm.is_valid():
            userForm.save()
            adduserForm.save()

            messages.success(request, 'Bloger updated successfully.')

            return redirect('super_admin/view_bloger')  # Replace 'success_url' with the desired URL
        else:
            messages.error(request, 'Error updating property owner. Please check the form.')
            print(userForm.errors)
            print(adduserForm.errors)
            return render(request,'update_blogers.html',{'adduserForm': adduserForm, 'userForm': userForm})
            
    else:
        userForm = Addblogger(instance=user, prefix='vender_user')
        adduserForm = AddBlogerForm(instance=vender, prefix='vender1')
    return render(request,'update_blogers.html',{'adduserForm': adduserForm, 'userForm': userForm})
 


@login_required(login_url='/login')
def category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('super_admin/view_category')
    else:
        form = CategoryForm()

    return render(request, 'category.html', {'form': form})

@login_required(login_url='/login')
def view_category(request):
    user = Category.objects.all()
    return render(request, 'view_category.html',{'user':user})

@login_required(login_url='/login')
def delete_category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('/super_admin/view_category')
   
@login_required(login_url='/login')
def update_category(request,pk):

    if request.method=="POST":
        pi=Category.objects.get(pk=pk)
        fm=CategoryForm(request.POST,request.FILES,instance=pi)
        if fm.is_valid():
            fm.save()
            return redirect('super_admin/view_category')
    else:
            pi=Category.objects.get(id=pk)
            fm=CategoryForm(instance=pi)
        
        # return render(request, 'edit.html')
    return render(request, 'update_category.html',{'fm':fm})


@login_required(login_url='/login')
def privacy_policy(request):
    existing_terms = Policy.objects.first()

    if request.method == 'POST':
        form = PrivacyForm(request.POST, instance=existing_terms)
        if form.is_valid():
            form.save()
            return redirect('super_admin/privacy_policy')
        else:
            messages.error(request, 'Error updating privacy policy. Please correct the errors below.')
    else:
        form = PrivacyForm(instance=existing_terms)

    user = Policy.objects.all()

    return render(request, 'privacy_policy.html', {'form': form, 'user': user, 'existing_terms': existing_terms})

@login_required(login_url='/login')
def delete_privacy_policy(request,id):
    u = Policy.objects.get(id=id)
    u.delete()
    return redirect('super_admin/privacy_policy') 


@login_required(login_url='/login')
def terms_condition(request):
    existing_terms = Terms.objects.first()

    if request.method == 'POST':
        form = TermsForm(request.POST, instance=existing_terms)
        if form.is_valid():
            form.save()
            return redirect('super_admin/terms')
    else:
        form = TermsForm(instance=existing_terms)

    user = Terms.objects.all()

    return render(request, 'terms_condition.html', {'form': form, 'user': user, 'existing_terms': existing_terms})

@login_required(login_url='/login')
def delete_terms(request,id):
    u = Terms.objects.get(id=id)
    u.delete()
    return redirect('super_admin/terms') 


# @login_required(login_url='/login')
# def notification(request):
#     return render(request, 'notification.html')


@login_required(login_url='/login')
def review(request):
    product=Product.objects.all()
    return render(request, 'product_preview.html',{'product':product})


@login_required (login_url='/login')
def delete_product1(request,id):
    user = Product.objects.get(id=id)
    user.delete()
    return redirect('super_admin/product_review')



@login_required(login_url='/login')
def notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('super_admin/notification')
    else:
        form = NotificationForm()

    return render(request, 'notification.html', {'form': form})