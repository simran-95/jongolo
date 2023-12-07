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
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('view')
    else:
        form = BlogForm()

    return render(request, 'blogs/add_blogs.html', {'form': form})




def view_blog(request):
    # user = Blog.objects.all()
    user = Blog.objects.filter(user=request.user)
    return render(request, 'blogs/view_blog.html',{'user':user})


def delete_blog(request, id):
    category = Blog.objects.get(id=id)
    category.delete()
    return redirect('view')
   

def update_blog(request,pk):

    if request.method=="POST":
        pi=Blog.objects.get(pk=pk)
        fm=BlogForm(request.POST,request.FILES,instance=pi)
        if fm.is_valid():
            fm.save(commit=False)
            fm.user = request.user
            fm.save()
            return redirect('view')
    else:
            pi=Blog.objects.get(id=pk)
            fm=BlogForm(instance=pi)
        
        # return render(request, 'edit.html')
    return render(request, 'blogs/update_blogs.html',{'fm':fm})