"""
URL configuration for GYM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from GymManagementSystem.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication
    path('', index, name='index'),
    path('logout/', Logout, name="logout"),  # Renamed for clarity
    path('user_logout/', user_logout, name="user_logout"),
    path('user_login/', user_login, name="user_login"),
    path('registration/', registration, name="registration"),
    
    # User Profile & Password
    path('user_profile/', user_profile, name="user_profile"),
    path('user_change_password/', user_change_password, name="user_change_password"),

    # Booking
    path('applyBooking/<int:pid>/', apply_booking, name="apply_booking"),  # Standardized naming
    path('booking_detail/<int:pid>/', booking_detail, name="booking_detail"),
    path('booking_history/', booking_history, name="booking_history"),
    path('new_booking/', new_booking, name='new_booking'),
    path('bookingReport/', bookingReport, name='bookingReport'),
    path('deleteBooking/<int:pid>/', deleteBooking, name='deleteBooking'),

    # Categories
    path('manageCategory/', manageCategory, name='manageCategory'),
    path('editCategory/<int:category_id>/', editCategory, name='editCategory'),  # Changed pid -> category_id
    path('deleteCategory/<int:category_id>/', deleteCategory, name='deleteCategory'),

    # Package Types
    path('managePackageType/', managePackageType, name='managePackageType'),
    path('editPackageType/<int:package_type_id>/', editPackageType, name='editPackageType'),  # Changed pid -> package_type_id
    path('deletePackageType/<int:package_type_id>/', deletePackageType, name='deletePackageType'),

    # Packages
    path('addPackage/', addPackage, name='addPackage'),  # Added missing `/`
    path('managePackage/', managePackage, name='managePackage'),
    path('editPackage/<int:package_id>/', editPackage, name='editPackage'),  # Changed pid -> package_id
    path('deletePackage/<int:package_id>/', deletePackage, name='deletePackage'),

    # User Management
    path('reg_user/', reg_user, name="reg_user"),
    path('delete_user/<int:user_id>/', delete_user, name="delete_user"),  # Changed pid -> user_id

    # Registration Report
    path('regReport/', regReport, name='regReport'),

    # Admin Dashboard
    path('admin_home/', admin_home, name='admin_home'),
    path('changePassword/', changePassword, name='changePassword'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
