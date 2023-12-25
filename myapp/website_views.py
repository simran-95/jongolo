from django.shortcuts import render,redirect,get_object_or_404
from .forms import *
from .models import *
from django.contrib.auth import login as dj_login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.conf import settings
import stripe
from django.views import View
from .models import Order as OrderModel
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse


stripe.api_key = 'sk_test_51OITjfSGqeyhk1pWAkeGPNjEevcHkTLHgSa56PfMqWH1ik4v6UbVv82jd4HYyXSNjGVlwl6vvwPfI8skyrpNdmke00zEEvqqu1'
stripe.api_key=settings.STRIPE_SECRET_KEY
STRIPE_PUBLC_KEY = settings.STRIPE_PUBLISHABLE_KEY,


def about(request):
    if request.user.is_authenticated:
        # If the user is authenticated, fetch the cart information
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)
        cart_count = cart_items.count()
    else:
        # If the user is not authenticated, set default values for cart information
        total_price = 0
        cart_count = 0
    return render(request, 'websiteuser/about.html',{'total_price': total_price, 'cart_count': cart_count})

def logout_view(request):
    logout(request)
    return redirect('/')

def dashboard2(request):
    print(request.user)
    cat = Product.objects.all()[:12]

    if request.user.is_authenticated:
        # If the user is authenticated, fetch the cart information
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)
        cart_count = cart_items.count()
    else:
        # If the user is not authenticated, set default values for cart information
        total_price = 0
        cart_count = 0

    return render(request, 'websiteuser/dashboard-web.html', {'cat': cat, 'total_price': total_price, 'cart_count': cart_count})


def header(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    cart_items = CartItem.objects.filter(user=request.user)
    cart_count = cart_items.count()
    print(cart_count)
    return render(request, 'websiteuser/header.html',{'cart_count':cart_count})
    
def base(request):
    # cart_items = CartItem.objects.filter(user=request.user)
    # total_price = sum(item.total_price() for item in cart_items)
    # cart_items = CartItem.objects.filter(user=request.user)
    # cart_count = cart_items.count()
    # print(cart_count)
    return render(request, 'websiteuser/base.html')


def product(request):
    product=Product.objects.all()
    categories=Category.objects.all()
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)
        cart_items = CartItem.objects.filter(user=request.user)
        cart_count = cart_items.count()
    else:
        # If the user is not authenticated, set default values for cart information
        total_price = 0
        cart_count = 0
    return render(request, 'websiteuser/product.html',{'categories':categories,'product':product,'cart_count':cart_count})


def product_cat(request,categoryid):
    # print(categoryid)
    categories=Category.objects.all()
    cats=Category.objects.get(pk=categoryid)

    product=Product.objects.filter(category=cats)
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)
        cart_items = CartItem.objects.filter(user=request.user)
        cart_count = cart_items.count()
    else:
        # If the user is not authenticated, set default values for cart information
        total_price = 0
        cart_count = 0

    context={'product':product,'categories':categories,'cart_count':cart_count}
    return render(request, 'websiteuser/product.html',context)
   

def product_single(request,id):
    product=Product.objects.filter(id=id)
    emp=Product.objects.all()

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)
        cart_items = CartItem.objects.filter(user=request.user)
        cart_count = cart_items.count()
    else:
        # If the user is not authenticated, set default values for cart information
        total_price = 0
        cart_count = 0

    
    return render(request, 'websiteuser/product-single.html', {'product':product,'emp':emp, 'cart_count':cart_count})


# ///////// Orders ///////////
from django.apps import apps

# def calculate_total_quantity(order):
#     order_items = OrderItem.objects.filter(order=order)
#     total_quantity = sum(item.quantity for item in order_items)
#     return total_quantity

# def calculate_total_price(order):
#     order_items = OrderItem.objects.filter(order=order)
#     total_price1 = sum(item.unit_price * item.quantity for item in order_items)
#     return total_price1

@login_required (login_url='/login1')
def Order_view(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    # total_earnings = sum(product.total_earnings() for product in user_products)
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)
        cart_items = CartItem.objects.filter(user=request.user)
        cart_count = cart_items.count()
    else:
        # If the user is not authenticated, set default values for cart information
        total_price = 0
        cart_count = 0
    # print(user_orders)  # Add this line to print user_orders
    return render(request, 'websiteuser/order.html', {'user_orders': user_orders,'cart_count':cart_count})

# ///////// Add To Cart ///////////


@login_required (login_url='/login1')
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    user = request.user

    # Check if the item is already in the cart for the user
    cart_item, created = CartItem.objects.get_or_create(user=user, product=product)

    # If the item is already in the cart, increment the quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_view')


@login_required (login_url='/login1')
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    cart_items = CartItem.objects.filter(user=request.user)

    # Ensure that item.total_price is a valid number
    # subtotal = sum([item.total_price() for item in cart_items])
    delivery_charge = 100.00 
    delivery_charge1 = "{:.2f}".format(delivery_charge) # Replace with your actual delivery charge
    discount = 3.00 
    discount1 = "{:.2f}".format(discount) # Replace with your actual discount

    # total = round(total_price + delivery_charge - discount, 2)
    total = "{:.2f}".format(total_price + delivery_charge - discount)
    print(total)
    # total_price = round(total_price, 2)
    total_price_formatted = "{:.2f}".format(total_price)
    cart_count = cart_items.count()

    return render(request, 'websiteuser/cart.html', {'cart_items': cart_items, 'total_price': total_price, 'delivery_charge1':delivery_charge1, 'discount1':discount1, 'total':total, 'total_price_formatted':total_price_formatted,'cart_count':cart_count})


@login_required (login_url='/login1')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')



@login_required (login_url='/login1')
def checkout(request: HttpRequest):
    print("Entering checkout view")
    print(request.user)
    total_price = 0.00
    
    try:
        add_user_instance = AddUser.objects.get(user=request.user)
        user_data = {
            'username': request.user.username,
            'email': request.user.email,
            'address': add_user_instance.address,
            'city': add_user_instance.city,
            'contact': add_user_instance.contact,
            # Add more fields as needed
        }

        cart_items = CartItem.objects.filter(user=request.user)

        # Ensure that item.total_price is a valid number
        subtotal = sum([item.total_price() for item in cart_items])
        delivery_charge = 100.00  # Replace with your actual delivery charge
        discount = 3.00  # Replace with your actual discount

        total_price = (subtotal + delivery_charge - discount)
        print(total_price)
        total_price = "{:.2f}".format(total_price)
    except AddUser.DoesNotExist:
        print(f"AddUser does not exist: {e}")
        # Handle the case when AddUser instance does not exist for the user
        user_data = {
            'username': request.user.username,
            'email': request.user.email,
            'address': '',
            'city': '',
            'contact': '',
            # Add more fields as needed
        }

    if request.method == 'POST' and request.user.is_authenticated:
        print("Processing POST request")
        country_id = request.POST.get('country')
        state_id = request.POST.get('state')
        city_id = request.POST.get('city')
        street_address = request.POST.get('street_address')  # Add this line
        postal_code = request.POST.get('postal_code')  # Add this line
        payment_mode = request.POST.get('payment_mode')  # Add this line

        try:
            country1 = Country.objects.get(id=country_id)
            state1 = State.objects.get(id=state_id)
            city1 = City.objects.get(id=city_id)
        except (Country.DoesNotExist, State.DoesNotExist, City.DoesNotExist):
            
            # Handle the case where one of the instances is not found
            messages.error(request, 'Invalid country, state, or city selected.')
            return redirect('checkout')

        # Create a new address for the user
        new_address = Address.objects.create(
            user=request.user,
            street_address=street_address,
            country=country1,
            state=state1,
            city=city1,
            postal_code=postal_code,
            payment_mode=payment_mode
        )

        # Create an order with the new address
        order = Order.objects.create(user=request.user, shipping_address=new_address, total_price=total_price)

        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.price
            )

        cart_items.delete()

        if payment_mode == 'stripe':
            return redirect('payment_form', order_id=order.id, total_price=total_price)
        else:
      
            messages.success(request, 'Your booking was successfully done.')
            return redirect('order')

    country2=Country.objects.all()

    return render(request, 'websiteuser/checkout.html', {'user_data': user_data, 'total_price':total_price,'cart_items':cart_items,'country2':country2})


@login_required (login_url='/login1')
def states(request):
    country_id = request.GET.get('country_id')
    # get_country= Country.objects.get(id=country_id)
    states = State.objects.filter(country_id=country_id).all()
    return render(request, 'websiteuser/states_dropdown_list_options.html', {'states': states})
    

@login_required (login_url='/login1')
def cities(request):
    state_id = request.GET.get('state_id')
    # get_state= State.objects.get(id=state_id)
    cities = City.objects.filter(state_id=state_id).all()
    return render(request, 'websiteuser/cities_dropdown_list_options.html', {'cities': cities})
   


class PaymentFormView(View):
    template_name = 'websiteuser/payment_form.html'

    def get(self, request, *args, **kwargs):
        publishable_key = settings.STRIPE_PUBLISHABLE_KEY
        order_id = kwargs.get('order_id')
        total_price = kwargs.get('total_price')
        return render(request, self.template_name, {'publishable_key': publishable_key, 'total_price': total_price})
       

    def post(self, request, *args, **kwargs):
        token = request.POST.get('stripeToken')

        try:
            # Create a source using the token
            source = stripe.Source.create(
                type='card',
                token=token,
            )

            # Use the created source in the PaymentIntent
            total_price = float(kwargs.get('total_price')) * 100

            charge = stripe.PaymentIntent.create(
                amount=int(total_price),  # Amount in cents
                currency='INR',
                description='Example charge',
                source=source.id,
            )
        except stripe.error.CardError as e:
            return render(request, 'websiteuser/payment_error.html')

        return render(request, 'websiteuser/payment_success.html')


def success_url(request):
    return render(request, 'websiteuser/payment_success.html') 


def error_url(request):
    return render(request, 'websiteuser/payment_error.html') 




# /////////////// for CancelReason ///////////////


from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest


@login_required (login_url='/login1')
def cancel_order(request, order_id):
    if request.method == 'POST':

        order = get_object_or_404(Order, id=order_id)

        # Check if the order is cancelable (pending or confirmed)
        if order.status in ['pending', 'confirmed']:
        # Check if a CancelReason already exists for this order
        
            cancel_reason, created = CancelReason.objects.get_or_create(order=order, user=request.user)

            # If it's not created, display an error message
            if not created:
                messages.error(request, 'Cancel reason already provided for this order.')
                return redirect('order')

            
            # Save the selected reason to the CancelReason model
            selected_reason = request.POST.get('reason')
            cancel_reason.reason = selected_reason
            cancel_reason.save()

            # return HttpResponse('Order canceled successfully.')
            messages.success(request, 'Order canceled successfully.')
            return redirect('order') # messages show in order page is remaining
        else:
            # return HttpResponseBadRequest('This order cannot be canceled.')
            messages.error(request, 'This order cannot be canceled.')
    return redirect('order')
    

@login_required(login_url='/login1')
def rating_products(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)

        if order.status in ['shipped', 'completed']:
            # Assuming each order has only one product
            product = order.orderitem_set.first().product

            rating, created = Rating.objects.get_or_create(order=order, user=request.user, product=product)

            if not created:
                messages.error(request, 'You rated already to this product!!.')
                return JsonResponse({'status': 'error', 'message': 'Already rated'})

            rating.rating = request.POST.get('rating')
            rating.review = request.POST.get('review')
            rating.save()

            messages.success(request, 'Rated successfully.')
            return JsonResponse({'status': 'success', 'message': 'Rating submitted successfully'})

        else:
            messages.error(request, 'This order cannot be Rated.')
            return JsonResponse({'status': 'error', 'message': 'Order cannot be rated'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def website_blog(request):
    user = Blog.objects.all()
    if request.user.is_authenticated:
        # If the user is authenticated, fetch the cart information
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)
        cart_count = cart_items.count()
    else:
        # If the user is not authenticated, set default values for cart information
        total_price = 0
        cart_count = 0
    return render(request, 'websiteuser/blog.html',{'user':user, 'cart_count':cart_count, 'total_price':total_price})



def user_sign_in(request):
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
            return HttpResponse('Successfully Added!!..')
        else:
            print(userForm.errors)
            print(receptionForm.errors)
        
    return render(request, 'websiteuser/register.html', context=mydict)



@login_required (login_url='/login1')
def profile(request):
    user_profile = AddUser.objects.get(user=request.user)

    if request.method == 'POST':
        fm = Adduser(request.POST, request.FILES, instance=request.user)
        form = AddUserForm(request.POST, request.FILES, instance=user_profile)
       
        if form.is_valid() and fm.is_valid():
            password = fm.cleaned_data.get('password')
            if password:
                request.user.set_password(password)
                update_session_auth_hash(request, request.user)
            form.save()
            fm.save()

            return redirect('profile')  # Redirect to the user's profile page after successful update
    else:
        form = AddUserForm(instance=user_profile)
        fm = Adduser(instance=request.user)

    return render(request, 'websiteuser/profile.html', {'form': form, 'fm':fm})


def contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Save the contact data to the database
            Contact.objects.create(name=name, email=email, subject=subject, message=message)

            # Send the email
            from_email = 'mahendraciss892@gmail.com'
            to = email

            try:
                msg = EmailMultiAlternatives(subject, message, from_email, [to])
                msg.send()
                return redirect('contact')
            except Exception as e:
                print(f"Error sending email: {e}")
                return render(request, 'websiteuser/contact.html', {'form': form, 'error': 'Error sending email'})
    else:
        form = ContactForm()

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)
        cart_count = cart_items.count()
    else:
        total_price = 0
        cart_count = 0

    return render(request, 'websiteuser/contact.html', {'form': form, }) 


def website_terms(request):
    terms = Terms.objects.all()
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)
        cart_count = cart_items.count()
    else:
        total_price = 0
        cart_count = 0
    
    return render(request, 'websiteuser/terms&condition.html',{'terms':terms, 'cart_count':cart_count, 'total_price':total_price}) 


def policies(request):
    terms = Policy.objects.all()
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.total_price() for item in cart_items)
        cart_count = cart_items.count()
    else:
        total_price = 0
        cart_count = 0
    return render(request, 'websiteuser/policies.html',{'terms':terms, 'cart_count':cart_count, 'total_price':total_price}) 


















    # if request.method=='POST':
    #     name=request.POST['name']
    #     email=request.POST['email']
    #     subject=request.POST['subject']
    #     message=request.POST['message']

        
    #     t = Contact(name=name, email=email, subject=subject, message=message)
    #     t.save()

    #     from_email = 'mahendraciss892@gmail.com'
      
    # #         # to = Developer.objects.get(project1=request.POST.get('project1'))
    #     to=email
    # #         # to='simranwachhani548@gmail.com'
    #     print(to)
    # #         # filesent = request.POST.get('filesent')
    #     msg = EmailMultiAlternatives(subject, message, from_email, [to])
    #     msg.send()
    #     return redirect('contact')
    # return render(request, 'websiteuser/contact.html')




    