from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib.auth import login as dj_login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def blogs(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_blog')
    else:
        form = BlogForm()

    return render(request, 'add_blog.html', {'form': form})



def view_blog(request):
    user = Blog.objects.all()
    return render(request, 'view_blog.html',{'user':user})


def delete_blog(request, id):
    category = Blog.objects.get(id=id)
    category.delete()
    return redirect('view_blog')
   

def update_blog(request,pk):

    if request.method=="POST":
        pi=Blog.objects.get(pk=pk)
        fm=BlogForm(request.POST,request.FILES,instance=pi)
        if fm.is_valid():
            fm.save()
            return redirect('view_blog')
    else:
            pi=Blog.objects.get(id=pk)
            fm=BlogForm(instance=pi)
        
        # return render(request, 'edit.html')
    return render(request, 'update_blog.html',{'fm':fm})