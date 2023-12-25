from django.contrib.auth.forms import UserCreationForm  ,UserChangeForm
from django.core.exceptions import ValidationError
from django import forms
from .models import *  
from django.forms import TimeInput

from django.forms import TimeField

class RequiredInput(forms.widgets.Input):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {})['required'] = 'required'
        super(RequiredInput, self).__init__(*args, **kwargs)
        
class UserForm(forms.ModelForm):
    username = forms.CharField(widget=RequiredInput())
         
    class Meta:
        model=User
        fields=('email','password','username')
        read_only_fields=['user_type']
   
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError("Email Already Exist")
        return email

class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",'username')


class Adduser(forms.ModelForm):
    # name =  forms.CharField(label=('Name'),widget=forms.TextInput(attrs={'class':'form-control','form-label':'User Name','placeholder': 'Enter Your Name'}))
    username = forms.CharField( label='UserName',widget=forms.TextInput(attrs={'class':'form-control','form-label':'User Name','placeholder': 'Enter Your Name'}),required=True)
    email = forms.EmailField(label='Email',required=True)
    # password = forms.CharField(label='Password',required=False)

    class Meta:
        model=User
        fields=['password','email','username']
        

class AddUserForm(forms.ModelForm):
   
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}),required=False)
    contact = forms.IntegerField()
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = AddUser
        fields = ['address', 'contact', 'profile_pic', 'city']
        exclude = ['created_at', 'updated_at', 'slug']



class Addvender(forms.ModelForm):
   
    username = forms.CharField( label='UserName',required=True)
    email = forms.EmailField(label='Email',required=True)
    password = forms.CharField( label='Password',required=False)

    class Meta:
        model=User
        fields=['password','email','username']
        

class AddVenderForm(forms.ModelForm):
   
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}),required=False)
    contact = forms.IntegerField()
    profile_pic = forms.ImageField(required=False)
    

    class Meta:
        model = Vender
        fields = ['address', 'contact', 'profile_pic', 'city']
        exclude = ['created_at', 'updated_at', 'slug']



class Addblogger(forms.ModelForm):
   
    username = forms.CharField( label='UserName',widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Your Name'}))
    email = forms.EmailField(label='Email',widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Your Email'}))
    password = forms.CharField(label='Password',widget=forms.TextInput(attrs={'class':'form-control','placeholder': 'Enter Your Password'}))

    class Meta:
        model=User
        fields=['password','email','username']
        

class AddBlogerForm(forms.ModelForm):
   
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
    contact = forms.IntegerField()
    profile_pic = forms.ImageField()

    class Meta:
        model = Blogger
        fields = ['address', 'contact', 'profile_pic', 'city']
        exclude = ['created_at', 'updated_at', 'slug']


# <--//////// end-up of login //////////-->


class CategoryForm(forms.ModelForm):
   
    name = forms.CharField( label='Category Name',required=True)
    image = forms.ImageField()

    class Meta:
        model = Category
        fields = ['name','image']
        

class ProductForm(forms.ModelForm):
   
    name = forms.CharField( label='Product Name',required=True)
    price = forms.IntegerField()
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Select Category'
    )
    description = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Description'
    )
    image = forms.ImageField()

    class Meta:
        model = Product
        fields = ['name','price','category','description','image']


class BlogForm(forms.ModelForm):
   
    title = forms.CharField( label='Blog Name',required=True)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
    image = forms.ImageField()

    class Meta:
        model = Blog
        fields = ['title','description','image']
        exclude = ['created_at']



class ContactForm(forms.ModelForm):

    name = forms.CharField( label='Name',required=True)
    email = forms.EmailField(label='Email',required=True)
    subject = forms.CharField(label='Subject',required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
   
    class Meta:
        model = Contact
        fields = ['name','email','subject','message']
        exclude = ['created_at']

from ckeditor.widgets import CKEditorWidget

class TermsForm(forms.ModelForm):
   
    # terms = forms.CharField( label='Terms and Condition',required=True)
    terms = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Terms
        fields = ['terms']
        
    
class PrivacyForm(forms.ModelForm):
   
    # terms = forms.CharField( label='Terms and Condition',required=True)
    terms = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Policy
        fields = ['terms']


class NotificationForm(forms.ModelForm):
    
    user = forms.ModelChoiceField(
        queryset=AddUser.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Select Category'
    )
    title = forms.CharField( label='Title',required=True)
    description = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Description'
    )


    class Meta:
        model = Notification
        fields = ['user','title','description']