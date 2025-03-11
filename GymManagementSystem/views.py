from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from random import randint
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash

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