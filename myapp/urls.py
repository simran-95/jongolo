from django.urls import path
from . import views,blogs_views
from . import vender_views,website_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('login', views.login,name='login'),
    path('admin-login', views.superadmin_login,name='admin-login'),
    # path('login2', views.vender_login,name='login2'),
    path('',views.vender_login,name='login1'),
    path('doLogin',views.doLogin,name='doLogin'),
    path('dologout',views.logout_view,name='logout'),
    path('base',views.base,name='base'),
   
    path('dashboard',views.dashboard,name='dashboard'),
    path('dashboard-add',views.dashboard1,name='dashboard-add'),
    path('dashboard-blog',views.dashboard3,name='dashboard-blog'),
    path('add_user',views.add_user,name='add_user'),
    path('view_user',views.view_user,name='view_user'),
    path('delete_user/<int:id>/',views.delete_user, name='delete_user'),
    path('update_user/<int:pk>',views.update_user,name='update_user'),
    path('profile', vender_views.profile,name='profile'),
    path('earning_admin', views.earning_admin,name='earning_admin'),
    
    # path('teacher_list',views.teacher_list,name='teacher_list'),
    # path('delete/<int:id>/', views.teacher_delete, name='delete'),
    path('add_vender',views.add_vendor,name='add_vender'),
    path('view_vender',views.view_vender,name='view_vender'),
    path('delete/<int:id>/',views.delete_vender, name='delete'),
    path('update-vender/<int:pk>',views.update_vender,name='update-vender'),
    #//////// bloggers views  /////////
    path('add_bloger',views.add_blogger,name='add_bloger'),
    path('view_bloger',views.view_blogger,name='view_bloger'),
    path('delete_bloger/<int:id>/',views.delete_blogger, name='delete_bloger'),
    path('update_bloger/<int:pk>',views.update_blogger,name='update_bloger'),

    #//////// blogs views  /////////
    path('blog',blogs_views.blogs,name='blog'),
    path('view',blogs_views.view_blog,name='view'),
    path('delete_blog/<int:id>/',blogs_views.delete_blog, name='delete_blog'),
    path('update_blog/<int:pk>',blogs_views.update_blog,name='update_blog'),


    #////// for category and product ///////
    path('category',views.category,name='category'),
    path('view_category',views.view_category,name='view_category'),
    path('delete_cat/<int:id>/', views.delete_category, name='delete_cat'),
    path('update_cat/<int:pk>',views.update_category,name='update_cat'),
    # path('product_single',views.product_single,name='product_single'),


    #////// for vender and product ///////
    path('add_product',vender_views.add_product,name='add_product'),
    path('view_product',vender_views.view_product,name='view_product'),
    path('delete_product/<int:id>/',vender_views.delete_product, name='delete_product'),
    path('update_product/<int:pk>',vender_views.update_product,name='update_product'),
    # path('/register',views.add_vendor,name='product'),
    path('earning',vender_views.earning,name='earning'),
    path('order1',vender_views.order_status,name='order1'),
    path('sign-in', vender_views.vender_sign_in, name='sign-in'),


    path('pending/<int:id>',vender_views.product_pending,name='pending'),
    path('confirmed/<int:id>',vender_views.product_confirm, name='confirmed'),
    path('placed/<int:id>',vender_views.product_placed, name='placed'),
    path('completed/<int:id>',vender_views.product_completed,name='completed'),
    path('completed/<int:id>',vender_views.product_completed,name='completed'),

    #//////// for Website and user /////////
    path('product',website_views.product,name='product'),
    path('product/<int:categoryid>',website_views.product_cat),
    path('details/<int:id>',website_views.product_single,name='details'),
    path('dashboard-web',website_views.dashboard2,name='dashboard-web'),
    path('header',website_views.header,name='header'),
    # path('cart/<int:product_id>/', website_views.cart, name='view_cart'),
    # path('view_cart/', website_views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', website_views.add_to_cart, name='add_to_cart'),
    path('cart_view/', website_views.cart_view, name='cart_view'),
    path('remove_from_cart/<int:item_id>/', website_views.remove_from_cart, name='remove_from_cart'),
    path('checkout', website_views.checkout, name='checkout'),
    path('order',website_views.Order_view,name='order'),
    # path('payment_form', website_views.HomePageView.as_view(), name='payment_form'),
    path('payment_form/<int:order_id>/<str:total_price>/', website_views.PaymentFormView.as_view(), name='payment_form'),
    path('cancel_order/<int:order_id>/', website_views.cancel_order, name='cancel_order'),
    path('sign-in1', website_views.user_sign_in, name='sign-in1'),

    path('blog1',website_views.website_blog,name='blog1'),
    path('contact',website_views.contact,name='contact'),
   
    # path('payment/', website_views.initiate_payment, name='payment'),
    
]
if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)