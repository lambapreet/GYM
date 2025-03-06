from django.db import models
from django.contrib.auth.models import User

# List of states and union territories in India
STATE_CHOICE = [
    ('ANDHRA PRADESH', 'Andhra Pradesh'),
    ('ARUNACHAL PRADESH', 'Arunachal Pradesh'),
    ('ASSAM', 'Assam'),
    ('BIHAR', 'Bihar'),
    ('CHHATTISGARH', 'Chhattisgarh'),
    ('GOA', 'Goa'),
    ('GUJARAT', 'Gujarat'),
    ('HARYANA', 'Haryana'),
    ('HIMACHAL PRADESH', 'Himachal Pradesh'),
    ('JHARKHAND', 'Jharkhand'),
    ('KARNATAKA', 'Karnataka'),
    ('KERALA', 'Kerala'),
    ('MADHYA PRADESH', 'Madhya Pradesh'),
    ('MAHARASHTRA', 'Maharashtra'),
    ('MANIPUR', 'Manipur'),
    ('MEGHALAYA', 'Meghalaya'),
    ('MIZORAM', 'Mizoram'),
    ('NAGALAND', 'Nagaland'),
    ('ODISHA', 'Odisha'),
    ('PUNJAB', 'Punjab'),
    ('RAJASTHAN', 'Rajasthan'),
    ('SIKKIM', 'Sikkim'),
    ('TAMIL NADU', 'Tamil Nadu'),
    ('TELANGANA', 'Telangana'),
    ('TRIPURA', 'Tripura'),
    ('UTTAR PRADESH', 'Uttar Pradesh'),
    ('UTTARAKHAND', 'Uttarakhand'),
    ('WEST BENGAL', 'West Bengal'),

    # Union Territories
    ('ANDAMAN AND NICOBAR ISLANDS', 'Andaman and Nicobar Islands'),
    ('CHANDIGARH', 'Chandigarh'),
    ('DADRA AND NAGAR HAVELI AND DAMAN AND DIU', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('DELHI', 'Delhi'),
    ('JAMMU AND KASHMIR', 'Jammu and Kashmir'),
    ('LADAKH', 'Ladakh'),
    ('LAKSHADWEEP', 'Lakshadweep'),
    ('PUDUCHERRY', 'Puducherry'),
]


class Category(models.Model):
    categoryname = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.categoryname if self.categoryname else "Unnamed Category"


class Packagetype(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    packagename = models.CharField(max_length=200, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.packagename if self.packagename else "Unnamed Package Type"


class Signup(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # OneToOneField for unique users
    mobile = models.CharField(max_length=10, null=True, blank=True)
    state = models.CharField(max_length=50, choices=STATE_CHOICE, default='UTTAR PRADESH')
    city = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name if self.user and self.user.first_name else "Unnamed User"


class Package(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    packagename = models.ForeignKey(Packagetype, on_delete=models.CASCADE, null=True, blank=True)
    titlename = models.CharField(max_length=100, null=True, blank=True)
    packageduration = models.CharField(max_length=100, null=True, blank=True)
    price = models.IntegerField()
    description = models.CharField(max_length=100, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titlename if self.titlename else "Unnamed Package"


STATUS = [
    (1, "Not Updated Yet"),
    (2, "Partial Payment"),
    (3, "Full Payment"),
]


class Booking(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True)
    register = models.ForeignKey(Signup, on_delete=models.CASCADE, null=True, blank=True)
    bookingnumber = models.CharField(max_length=100, null=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=1)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.bookingnumber}" if self.bookingnumber else "Unnamed Booking"


class Paymenthistory(models.Model):
    user = models.ForeignKey(Signup, on_delete=models.CASCADE, null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    price = models.CharField(max_length=100, null=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=1)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.price}" if self.price else "Unnamed Payment"



'''
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
STATE_CHOICE = [
    ('ANDHRA PRADESH', 'Andhra Pradesh'),
    ('ARUNACHAL PRADESH', 'Arunachal Pradesh'),
    ('ASSAM', 'Assam'),
    ('BIHAR', 'Bihar'),
    ('CHHATTISGARH', 'Chhattisgarh'),
    ('GOA', 'Goa'),
    ('GUJARAT', 'Gujarat'),
    ('HARYANA', 'Haryana'),
    ('HIMACHAL PRADESH', 'Himachal Pradesh'),
    ('JHARKHAND', 'Jharkhand'),
    ('KARNATAKA', 'Karnataka'),
    ('KERALA', 'Kerala'),
    ('MADHYA PRADESH', 'Madhya Pradesh'),
    ('MAHARASHTRA', 'Maharashtra'),
    ('MANIPUR', 'Manipur'),
    ('MEGHALAYA', 'Meghalaya'),
    ('MIZORAM', 'Mizoram'),
    ('NAGALAND', 'Nagaland'),
    ('ODISHA', 'Odisha'),
    ('PUNJAB', 'Punjab'),
    ('RAJASTHAN', 'Rajasthan'),
    ('SIKKIM', 'Sikkim'),
    ('TAMIL NADU', 'Tamil Nadu'),
    ('TELANGANA', 'Telangana'),
    ('TRIPURA', 'Tripura'),
    ('UTTAR PRADESH', 'Uttar Pradesh'),
    ('UTTARAKHAND', 'Uttarakhand'),
    ('WEST BENGAL', 'West Bengal'),
    
    # Union Territories
    ('ANDAMAN AND NICOBAR ISLANDS', 'Andaman and Nicobar Islands'),
    ('CHANDIGARH', 'Chandigarh'),
    ('DADRA AND NAGAR HAVELI AND DAMAN AND DIU', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('DELHI', 'Delhi'),
    ('JAMMU AND KASHMIR', 'Jammu and Kashmir'),
    ('LADAKH', 'Ladakh'),
    ('LAKSHADWEEP', 'Lakshadweep'),
    ('PUDUCHERRY', 'Puducherry'),
]


class Category(models.Model):
    categoryname = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    creationdate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.categoryname
    
    
class Packagetype(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    packagename = models.CharField(max_length=200, null=True)
    creationdate = models.DateTimeField(auto_now_add=True)  
    
    def __str__(self):
        return self.packagename
    
class Signup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=10, null=True)
    state = models.CharField(max_length=50,choices=STATE_CHOICE, default='UTTAR PRADESH')
    city = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=100,null=True)
    creationdate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.first_name
    
class Package(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    packagename = models.ForeignKey(Packagetype, on_delete=models.CASCADE, null=True)
    titlename = models.CharField(max_length=100, null=True)
    packageduration = models.CharField(max_length=100, null=True)
    price = models.IntegerField()
    description = models.CharField(max_length=100, null=True)
    creationdate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titlename
    
STATUS = ((1, "Not Updated Yet"), (2, "Partial Payment"), (3, 'Full Payment'))

class Booking(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True)
    register = models.ForeignKey(Signup, on_delete=models.CASCADE, null=True, blank=True)
    bookingnumber = models.CharField(max_length=100, null=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=1)
    creationdate = models.DateTimeField(auto_now_add=True)
    
class Paymenthistory(models.Model):
    user = models.ForeignKey(Signup, on_delete=models.CASCADE, null=True, blank=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    price = models.CharField(max_length=100, null=True, blank=True)
    status = models.IntegerField(choices=STATUS, default=1)
    creationdate = models.DateTimeField(auto_now_add=True)
    

'''