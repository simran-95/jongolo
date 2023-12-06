from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth import login as dj_login, logout, authenticate
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import update_session_auth_hash

# Create your views here.

def login(request):
    return render(request, 'admin-login.html')

def login1(request):
    return render(request, 'websiteuser/website-login.html')

# def product_single(request):
#     return render(request, 'websiteuser/product-single.html')
def superadmin_login(request):
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
           
            if user_type==User.VENDER:
               
                return redirect('dashboard-add')
            elif user_type==User.ADDUSER:
               
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
def dashboard(request):
    return render(request, 'index.html')

def dashboard1(request):
    return render(request, 'vender/dashboard-add.html')

def dashboard3(request):
    return render(request, 'vender/dashboard-blog.html')
    
def base(request):
    return render(request, 'websiteuser/base.html')


def logout_view(request):
    logout(request)
    return redirect('/')


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
            return redirect('view_user')
        else:
            print(userForm.errors)
            print(receptionForm.errors)
        
    return render(request, 'add_user.html', context=mydict)


def view_user(request):
    user = AddUser.objects.all()
    return render(request, 'view_user.html',{'user':user})


def delete_user(request,id):
    u = AddUser.objects.get(id=id)
    u.delete()
    return redirect('view_user')
    


def update_user(request,pk):
    add=AddUser.objects.get(id=pk)
    user=User.objects.get(id=add.user_id)

    userForm=Adduser(instance=user)
    adduserForm=AddUserForm(request.FILES,instance=add)
    mydict={'userForm':userForm,'adduserForm':adduserForm}
    if request.method=='POST':
        userForm=Adduser(request.POST,instance=user)
        adduserForm=AddUserForm(request.POST,request.FILES,instance=add)
        if userForm.is_valid() and adduserForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            add=adduserForm.save(commit=False)
            add.status=True
            add.save()
            return redirect('view_user')
        else:
            userForm = Adduser(instance=user)
            adduserForm = AddUserForm(instance=add)
    return render(request,'update_user.html',{'adduserForm': adduserForm, 'userForm': userForm})


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
            return redirect('view_vender')
        else:
             print(userForm.errors)
             print(receptionForm.errors)
        
    return render(request, 'add_vender.html', context=mydict)


def view_vender(request):
    user = Vender.objects.all()
    return render(request, 'view_vender.html',{'user':user})


def delete_vender(request,id):
    u = Vender.objects.get(id=id)
    u.delete()
    return redirect('view_vender')
    


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
            return redirect('view_vender')  # Replace 'success_url' with the desired URL
        else:
            print(pharmacist_user_form.errors)
            print(pharmacist_form.errors)
    else:
        pharmacist_user_form = Addvender(instance=user, prefix='vender_user')
        pharmacist_form = AddVenderForm(instance=vender, prefix='vender1')
    
    return render(request, 'update_vender.html', {'pharmacist_user_form': pharmacist_user_form, 'pharmacist_form': pharmacist_form})



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

            return redirect('view_bloger')
        else:
            print(userForm.errors)
            print(bloggerForm.errors)
            return render(request, 'add_bloger.html', context=mydict)
    
    return render(request, 'add_bloger.html', context=mydict)


def view_blogger(request):
    user = Blogger.objects.all()
    return render(request, 'view_bloger.html',{'user':user})


def delete_blogger(request,id):
    u = Blogger.objects.get(id=id)
    u.delete()
    return redirect('view_bloger')   


def update_blogger(request,pk):
    add=Addblogger.objects.get(id=pk)
    user=User.objects.get(id=add.user_id)

    userForm=Addblogger(instance=user)
    adduserForm=AddBlogerForm(request.FILES,instance=add)
    mydict={'userForm':userForm,'adduserForm':adduserForm}
    if request.method=='POST':
        userForm=Addblogger(request.POST,instance=user)
        adduserForm=AddBlogerForm(request.POST,request.FILES,instance=add)
        if userForm.is_valid() and adduserForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            add=adduserForm.save(commit=False)
            add.status=True
            add.save()
            return redirect('view_user')
        else:
            userForm = Addblogger(instance=user)
            adduserForm = AddBlogerForm(instance=add)
    return render(request,'update_bloger.html',{'adduserForm': adduserForm, 'userForm': userForm})



def category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_category')
    else:
        form = CategoryForm()

    return render(request, 'category.html', {'form': form})


def view_category(request):
    user = Category.objects.all()
    return render(request, 'view_category.html',{'user':user})


def delete_category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('/view_category')
   

def update_category(request,pk):

    if request.method=="POST":
        pi=Category.objects.get(pk=pk)
        fm=CategoryForm(request.POST,request.FILES,instance=pi)
        if fm.is_valid():
            fm.save()
            return redirect('view_category')
    else:
            pi=Category.objects.get(id=pk)
            fm=CategoryForm(instance=pi)
        
        # return render(request, 'edit.html')
    return render(request, 'update_category.html',{'fm':fm})


# def update_category(request,pk):
#     # vender=Category.objects.get(id=pk)
#     # userForm=CategoryForm(request.FILES,instance=vender)
   
#     # mydict={'userForm':userForm}
#     if request.method=='POST':
#         vender=Category.objects.get(pk=pk)
#         userForm=CategoryForm(request.POST,request.FILES,instance=vender)
#         if userForm.is_valid():
#             userForm.save()
#             return redirect('view_category')
#         else:
#             vender=Category.objects.get(pk=pk)
#             userForm=CategoryForm(instance=vender)
#     return render(request,'update_category.html',{'userForm':userForm})
