from django.contrib import admin
from .models import *
from .forms import UserCreationForm,UserChangeForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ("email", "is_staff", "is_active",'username','user_type')
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password",'username','user_type')}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(User, CustomUserAdmin)
admin.site.register(AddUser)
admin.site.register(Vender)
admin.site.register(Blogger)

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Blog)

admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)

admin.site.register(Adres)
admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(CancelReason)
admin.site.register(Contact)

