from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from random import randint
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from django.db import IntegrityError
from django.http import JsonResponse
from datetime import datetime, timedelta
from .utils import random_with_N_digits  


# Create your views here.



def index(request):
    if request.method == "POST":
        u = request.POST.get('uname', '').strip()  
        p = request.POST.get('pwd', '').strip()
        
        user = authenticate(username=u, password=p)
        
        if user:
            if user.is_active:  
                login(request, user)
                messages.success(request, "Logged In Successfully")
                return redirect('admin_home' if user.is_staff else 'user_dashboard')
            else:
                messages.error(request, "Your account is inactive. Contact admin.")
        else:
            messages.error(request, "Invalid Username or Password. Please try again.")

        return redirect('index') 

#This Django ORM query retrieves the first 5 records from the Package model, ordered by the id field in ascending order
    package = Package.objects.order_by('id')[:5] 
    return render(request, 'index.html', {'package': package})  

def registration(request):
    if request.method == "POST":
        fname = request.POST.get('firstname')
        lname = request.POST.get('secondname')
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('registration')

        user = User.objects.create_user(first_name=fname, last_name=lname, email=email, password=pwd, username=email)
        Signup.objects.create(user=user, mobile=mobile, address=address)

        messages.success(request, "Registration Successful. Please login.")
        return redirect('user_login')

    return render(request, 'registration.html')

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email') 
        pwd = request.POST.get('password')

        user = authenticate(username=email, password=pwd)

        if not user:
            messages.error(request, "Invalid email or password")
            return redirect('user_login')

        if user.is_staff:  
            messages.error(request, "Staff login not allowed here")
            return redirect('user_login')

        login(request, user)
        messages.success(request, "User Login Successful")
        return redirect('index')

    return render(request, 'user_login.html')

@login_required(login_url='admin_login') 
def admin_home(request):
    context = {
        "totalcategory": Category.objects.count(),
        "totalpackagetype": Packagetype.objects.count(),
        "totalpackage": Package.objects.count(),
        "totalbooking": Booking.objects.count(),
        "New": Booking.objects.filter(status="1"),
        "Partial": Booking.objects.filter(status="2"),
        "Full": Booking.objects.filter(status="3"),
    }
    return render(request, 'admin/admin_home.html', context)

def Logout(request):
    logout(request)  
    messages.success(request, "Logout Successfully")  
    return redirect('index')

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out successfully.")
    return redirect(reverse('index'))

def user_profile(request):
    if request.method == "POST":
        # Safely retrieve form values
        fname = request.POST.get('firstname', '').strip()
        lname = request.POST.get('secondname', '').strip()
        email = request.POST.get('email', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        address = request.POST.get('address', '').strip()

        # Validate that the user exists
        user = request.user
        if user.is_authenticated:
            # Update User model
            User.objects.filter(id=user.id).update(first_name=fname, last_name=lname, email=email)

            # Update or create Signup model data
            signup, created = Signup.objects.get_or_create(user=user)
            signup.mobile = mobile
            signup.address = address
            signup.save()

            messages.success(request, "Profile updated successfully.")
        else:
            messages.error(request, "You must be logged in to update your profile.")

        return redirect('user_profile')

    # Fetch user data safely
    data = get_object_or_404(Signup, user=request.user)
    return render(request, "user_profile.html", {"data": data})

def user_change_password(request):
    if request.method == "POST":
        old_password = request.POST['pwd1']  # Old password
        new_password = request.POST['pwd2']  # New password
        confirm_password = request.POST['pwd3']  # Confirm password

        user = request.user

        # Check if the old password is correct
        if not user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect('user_change_password')

        # Check if new password matches confirmation
        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return redirect('user_change_password')

        # Change password
        user.set_password(new_password)
        user.save()

        # Keep user logged in after password change
        update_session_auth_hash(request, user)

        messages.success(request, "Password changed successfully.")
        return redirect('user_profile')  # Redirect to profile or login page

    return render(request, 'user_change_password.html')

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)  # Restrict to admins
def manageCategory(request):
    category = Category.objects.all()
    error = None  # Default value

    if request.method == "POST":
        categoryname = request.POST.get('categoryname', '').strip()

        if not categoryname:
            messages.error(request, "Category name cannot be empty.")
            return redirect('manageCategory')

        # Check if category already exists
        if Category.objects.filter(categoryname__iexact=categoryname).exists():
            messages.error(request, "Category already exists.")
            return redirect('manageCategory')

        try:
            Category.objects.create(categoryname=categoryname)
            messages.success(request, "Category added successfully!")
        except Exception as e:
            messages.error(request, f"Error adding category: {str(e)}")

    return render(request, 'admin/manageCategory.html', {"category": category})

@login_required
@user_passes_test(is_admin)  # Restrict to admins
def editCategory(request, pid):
    category = get_object_or_404(Category, id=pid)  # Handle invalid IDs

    if request.method == "POST":
        categoryname = request.POST.get('categoryname', '').strip()

        if not categoryname:
            messages.error(request, "Category name cannot be empty.")
            return redirect('editCategory', pid=pid)

        # Check if a category with the same name already exists (excluding the current one)
        if Category.objects.filter(categoryname__iexact=categoryname).exclude(id=pid).exists():
            messages.error(request, "Category with this name already exists.")
            return redirect('editCategory', pid=pid)

        # Save the updated category
        try:
            category.categoryname = categoryname
            category.save()
            messages.success(request, "Category updated successfully!")
            return redirect('manageCategory')  # Redirect to category list
        except Exception as e:
            messages.error(request, f"Error updating category: {str(e)}")

    return render(request, 'admin/editCategory.html', {"category": category})


@login_required
@user_passes_test(is_admin)  # Restrict to admins
def deleteCategory(request, pid):
    category = get_object_or_404(Category, id=pid)  # Handle invalid IDs

    try:
        category.delete()
        messages.success(request, "Category deleted successfully!")
    except Exception as e:
        messages.error(request, f"Error deleting category: {str(e)}")

    return redirect('manageCategory')  # Redirect back to category list

@login_required(login_url='/admin_login/')  # Ensures user is logged in
@user_passes_test(is_admin, login_url='/admin_login/')  # Ensures user is an admin
def reg_user(request):
    data = Signup.objects.all()
    return render(request, "admin/reg_user.html", {"data": data})

@login_required(login_url='/admin_login/')
@user_passes_test(is_admin, login_url='/admin_login/')  # Restrict to admins
def delete_user(request, pid):
    user_profile = get_object_or_404(Signup, id=pid)  # Handle invalid IDs

    # Delete the associated User record
    try:
        user = user_profile.user  # Assuming a OneToOneField in Signup linking to User
        user.delete()
        messages.success(request, "User deleted successfully!")
    except Exception as e:
        messages.error(request, f"Error deleting user: {str(e)}")

    return redirect('reg_user')  # Redirect back to the user list



@login_required(login_url='admin_login')
def managePackageType(request):
    package = Packagetype.objects.all()
    category = Category.objects.all()
    error = None  # Initialize error variable

    if request.method == "POST":
        cid = request.POST.get('category')
        packagename = request.POST.get('packagename')

        if cid and packagename:  # Validate input
            try:
                category_instance = Category.objects.get(id=cid)
                Packagetype.objects.create(category=category_instance, packagename=packagename)
                error = "no"
            except Category.DoesNotExist:
                error = "invalid_category"
            except IntegrityError:
                error = "yes"
        else:
            error = "missing_fields"

    context = {
        'package': package,
        'category': category,
        'error': error
    }
    return render(request, 'admin/managePackageType.html', context)


@login_required(login_url='admin_login')
def editPackageType(request, pid):
    package = get_object_or_404(Packagetype, id=pid)
    category = Category.objects.all()
    error = None  # Initialize error variable

    if request.method == "POST":
        cid = request.POST.get('category')
        packagename = request.POST.get('packagename')

        if cid and packagename:  # Validate input
            try:
                category_instance = Category.objects.get(id=cid)
                package.category = category_instance
                package.packagename = packagename
                package.save()
                error = "no"
            except Category.DoesNotExist:
                error = "invalid_category"
            except IntegrityError:
                error = "yes"
        else:
            error = "missing_fields"

    context = {
        'package': package,
        'category': category,
        'error': error
    }
    return render(request, 'admin/editPackageType.html', context)

@login_required(login_url='admin_login')
def deletePackageType(request, pid):
    if request.method == "POST":  # Ensure deletion is via POST
        package = get_object_or_404(Packagetype, id=pid)
        package.delete()
    return redirect('managePackageType')


@login_required(login_url='admin_login')
def addPackage(request):
    categories = Category.objects.all()
    packages = Packagetype.objects.all()
    error = None  # Initialize error variable

    if request.method == "POST":
        cid = request.POST.get('category')
        package_id = request.POST.get('packagename')
        titlename = request.POST.get('titlename')
        duration = request.POST.get('duration')
        price = request.POST.get('price')
        description = request.POST.get('description')

        if cid and package_id and titlename and duration and price and description:
            try:
                category_instance = get_object_or_404(Category, id=cid)
                package_instance = get_object_or_404(Packagetype, id=package_id)

                Package.objects.create(
                    category=category_instance,
                    packagename=package_instance,
                    titlename=titlename,
                    packageduration=duration,
                    price=price,
                    description=description
                )
                error = "no"
            except IntegrityError:
                error = "yes"
        else:
            error = "missing_fields"

    context = {
        'categories': categories,
        'packages': packages,
        'error': error
    }
    return render(request, 'admin/addPackage.html', context)

@login_required(login_url='admin_login')
def managePackage(request):
    packages = Package.objects.all()
    context = {'packages': packages}
    return render(request, 'admin/managePackage.html', context)

@login_required(login_url='/user_login/')
def booking_history(request):
    try:
        user_signup = Signup.objects.get(user=request.user)  # Fetch Signup instance
        bookings = Booking.objects.filter(register=user_signup)  # Get user's bookings
    except Signup.DoesNotExist:
        bookings = None  # Handle case where user has no Signup record

    context = {'bookings': bookings}
    return render(request, "booking_history.html", context)

def is_admin(user):
    return user.is_staff  # Ensures only staff can access

@login_required(login_url='/admin_login/')
@user_passes_test(is_admin, login_url='/booking_history/')
def new_booking(request):
    action = request.GET.get('action')
    
    # Default query
    data = Booking.objects.all()

    # Filter based on status
    status_filter = {"New": "1", "Partial": "2", "Full": "3"}
    if action in status_filter:
        data = data.filter(status=status_filter[action])

    context = {"bookings": data, "action": action}
    return render(request, "admin/new_booking.html", context)


@login_required(login_url='/user_login/')
def booking_detail(request, pid):
    booking = get_object_or_404(Booking, id=pid)
    payment_history = Paymenthistory.objects.filter(booking=booking)

    if request.method == "POST":
        price = request.POST.get('price')
        status = request.POST.get('status')

        if not price or not status:
            messages.error(request, "Price and Status are required fields.")
        else:
            try:
                price = float(price)  # Ensure price is a valid number
                booking.status = status
                booking.save()
                Paymenthistory.objects.create(booking=booking, price=price, status=status)
                messages.success(request, "Action Updated")
                return redirect('booking_detail', pid=pid)
            except ValueError:
                messages.error(request, "Invalid price value.")
            except IntegrityError:
                messages.error(request, "Error updating payment history.")

    context = {
        "booking": booking,
        "payment_history": payment_history
    }

    if request.user.is_staff:
        return render(request, "admin/admin_booking_detail.html", context)
    else:
        return render(request, "user_booking_detail.html", context)


def is_admin(user):
    return user.is_staff  # Ensures only staff can access

@login_required(login_url='/admin_login/')
@user_passes_test(is_admin, login_url='/')
def editPackage(request, pid):
    package_instance = get_object_or_404(Package, id=pid)
    categories = Category.objects.all()
    packagetypes = Packagetype.objects.all()

    if request.method == "POST":
        cid = request.POST.get('category')
        packagename_id = request.POST.get('packagename')
        titlename = request.POST.get('titlename')
        duration = request.POST.get('duration')
        price = request.POST.get('price')
        description = request.POST.get('description')

        try:
            selected_category = get_object_or_404(Category, id=cid)
            selected_package_type = get_object_or_404(Packagetype, id=packagename_id)

            # Validate price
            try:
                price = float(price)
            except ValueError:
                messages.error(request, "Invalid price format.")
                return redirect('editPackage', pid=pid)

            # Update package
            package_instance.category = selected_category
            package_instance.packagename = selected_package_type
            package_instance.titlename = titlename
            package_instance.packageduration = duration
            package_instance.price = price
            package_instance.description = description

            package_instance.save()
            messages.success(request, "Package updated successfully!")
            return redirect('managePackage')

        except IntegrityError:
            messages.error(request, "Error updating package. Please try again.")

    context = {
        "package": package_instance,
        "categories": categories,
        "packagetypes": packagetypes
    }
    return render(request, "admin/editPackage.html", context)


@login_required(login_url='/admin_login/')  # Ensures only logged-in users can access
def load_subcategory(request):
    category_id = request.GET.get('category')

    if not category_id:
        return JsonResponse({"error": "Category ID is required"}, status=400)

    # Fetch subcategories safely
    subcategories = Package.objects.filter(category=category_id).order_by('packagename').values('id', 'packagename')

    return JsonResponse(list(subcategories), safe=False)

def is_admin(user):
    return user.is_staff

@login_required(login_url='/admin_login/')
@user_passes_test(is_admin, login_url='/')
def deletePackage(request, pid):
    package = get_object_or_404(Package, id=pid)
    package.delete()
    messages.success(request, "Package deleted successfully.")
    return redirect('managePackage')

@login_required(login_url='/admin_login/')
@user_passes_test(is_admin, login_url='/')
def deleteBooking(request, pid):
    booking = get_object_or_404(Booking, id=pid)
    booking.delete()
    messages.success(request, "Booking deleted successfully.")
    return redirect('new_booking')


@login_required(login_url='/admin_login/')
@user_passes_test(is_admin, login_url='/')
def bookingReport(request):
    data = None
    data2 = False  # More meaningful name instead of `data2`
    
    if request.method == "POST":
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')

        if not fromdate or not todate:
            messages.error(request, "Both dates are required.")
        else:
            try:
                # Convert string dates to datetime objects
                from_date = datetime.strptime(fromdate, "%Y-%m-%d")
                to_date = datetime.strptime(todate, "%Y-%m-%d") + timedelta(days=1)  # Include full to_date

                # Fetch bookings within date range
                data = Booking.objects.filter(creationdate__gte=from_date, creationdate__lt=to_date)
                data2 = True
            except ValueError:
                messages.error(request, "Invalid date format. Please enter valid dates.")

    context = {
        "data": data,
        "data2": data2
    }
    return render(request, "admin/bookingReport.html", context)


@login_required(login_url='/admin_login/')
@user_passes_test(is_admin, login_url='/')
def regReport(request):
    data = None
    data_available = False  # Better variable name instead of `data2`
    
    if request.method == "POST":
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')

        if not fromdate or not todate:
            messages.error(request, "Both dates are required.")
        else:
            try:
                # Convert date strings to datetime objects
                from_date = datetime.strptime(fromdate, "%Y-%m-%d")
                to_date = datetime.strptime(todate, "%Y-%m-%d") + timedelta(days=1)  # Include full to_date

                # Fetch signups within date range
                data = Signup.objects.filter(creationdate__gte=from_date, creationdate__lt=to_date)
                data_available = True
            except ValueError:
                messages.error(request, "Invalid date format. Please enter valid dates.")

    context = {
        "data": data,
        "data_available": data_available
    }
    return render(request, "admin/regReport.html", context)


@login_required(login_url='/admin_login/')
def changePassword(request):
    if request.method == "POST":
        old_password = request.POST.get('oldpassword')
        new_password = request.POST.get('newpassword')

        if not old_password or not new_password:
            messages.error(request, "All fields are required.")
            return redirect('changePassword')

        user = request.user

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Prevents logout after password change
            messages.success(request, "Password changed successfully.")
            return redirect('changePassword')
        else:
            messages.error(request, "Incorrect old password.")

    return render(request, 'admin/changePassword.html')


def random_with_N_digits(n):
    if n <= 0:
        raise ValueError("Number of digits must be greater than 0")
    
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


@login_required(login_url='/user_login/')
def apply_booking(request, pid):
    package = get_object_or_404(Package, id=pid)
    register = get_object_or_404(Signup, user=request.user)

    # Prevent duplicate booking for the same package
    if Booking.objects.filter(package=package, register=register).exists():
        messages.error(request, "You have already booked this package.")
        return redirect('booking_history')

    # Create the booking
    booking = Booking.objects.create(
        package=package, 
        register=register, 
        bookingnumber=random_with_N_digits(10)
    )
    
    messages.success(request, "Booking Applied Successfully!")
    return redirect('booking_history')  # Redirect to a meaningful page
