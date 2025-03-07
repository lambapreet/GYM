from django.contrib import admin
from .models import Packagetype, Booking, Category, Package, Signup, Paymenthistory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'categoryname', 'status', 'creationdate')
    search_fields = ('categoryname', 'status')
    list_filter = ('status', 'creationdate')
    readonly_fields = ('creationdate',)

@admin.register(Packagetype)
class PackagetypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'packagename', 'category', 'creationdate')
    search_fields = ('packagename',)
    list_filter = ('creationdate',)
    readonly_fields = ('creationdate',)

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'titlename', 'packagename', 'category', 'price', 'packageduration', 'creationdate')
    search_fields = ('titlename', 'packagename__packagename', 'category__categoryname')
    list_filter = ('category', 'creationdate')
    readonly_fields = ('creationdate',)

@admin.register(Signup)
class SignupAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'mobile', 'state', 'city', 'address', 'creationdate')
    search_fields = ('user__first_name', 'user__username', 'mobile', 'city')
    list_filter = ('state', 'creationdate')
    readonly_fields = ('creationdate',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'package', 'register', 'bookingnumber', 'status', 'creationdate')
    search_fields = ('bookingnumber', 'register__user__first_name', 'register__mobile')
    list_filter = ('status', 'creationdate')
    readonly_fields = ('creationdate',)

@admin.register(Paymenthistory)
class PaymenthistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'booking', 'price', 'status', 'creationdate')
    search_fields = ('user__user__first_name', 'booking__bookingnumber', 'price')
    list_filter = ('status', 'creationdate')
    readonly_fields = ('creationdate',)


'''
from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Packagetype)
admin.site.register(Booking)
admin.site.register(Category)
admin.site.register(Package)
admin.site.register(Signup)
admin.site.register(Paymenthistory)

'''