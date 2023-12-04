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


stripe.api_key = 'sk_test_51OITjfSGqeyhk1pWAkeGPNjEevcHkTLHgSa56PfMqWH1ik4v6UbVv82jd4HYyXSNjGVlwl6vvwPfI8skyrpNdmke00zEEvqqu1'
stripe.api_key=settings.STRIPE_SECRET_KEY
STRIPE_PUBLC_KEY = settings.STRIPE_PUBLISHABLE_KEY,

def dashboard2(request):
    print(request.user)
    cat=Product.objects.all()[:12]
    # cats=Category.objects.get(pk=categoryid)
    # product=Blog.objects.filter(category=cats)
    return render(request, 'websiteuser/dashboard-web.html',{'cat':cat})


    
def base(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    cart_items = CartItem.objects.filter(user=request.user)
    cart_count = cart_items.count()
    return render(request, 'websiteuser/base.html',{'cart_count':cart_count})



def product(request):
    product=Product.objects.all()
    categories=Category.objects.all()

    return render(request, 'websiteuser/product.html',{'categories':categories,'product':product})


def product_cat(request,categoryid):
    # print(categoryid)
    categories=Category.objects.all()
    cats=Category.objects.get(pk=categoryid)

    product=Product.objects.filter(category=cats)
    context={'product':product,'categories':categories}
    return render(request, 'websiteuser/product.html',context)


def product_single(request,id):
    product=Product.objects.filter(id=id)
    emp=Product.objects.all()
    return render(request, 'websiteuser/product-single.html', {'product':product,'emp':emp})




# ///////// Add To Cart ///////////


@login_required
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

@login_required
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



@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')


# def checkout(request):
#     return render(request, 'websiteuser/checkout.html')

def checkout(request: HttpRequest):
    print(request.user)
    
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
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        street_address = request.POST.get('street_address')
        postal_code = request.POST.get('postal_code')

        # Create a new address for the user
        new_address = Adres.objects.create(
            user=request.user,
            street_address=street_address,
            country=country,
            state=state,
            city=city,
            postal_code=postal_code
        )

        # Create an order with the new address
       # Create an order with the new address
        order = Order.objects.create(user=request.user, shipping_address=new_address, total_price=total_price)

        # Add order items to the order (assuming you have a way to get cart items)
        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                unit_price=cart_item.product.price
            )

        # Optionally, you may want to clear the user's cart after creating the order
        cart_items.delete()

        # Redirect to payment_form with the required arguments
        return redirect('payment_form', order_id=order.id, total_price=total_price)




    # If it's a GET request or shipping address is not provided, render the checkout page with address form
    return render(request, 'websiteuser/checkout.html', {'user_data': user_data, 'total_price':total_price,'cart_items':cart_items})



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









# def payment_form(request):
#     key = settings.STRIPE_PUBLIC_KEY
#     return render(request, 'payment_form.html', {'stripe_public_key': stripe_public_key})