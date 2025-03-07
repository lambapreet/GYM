from django import forms
from .models import Booking
from django.contrib.auth.forms import UserCreationForm

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking  # Corrected 'models' to 'model'
        fields = ('bookingnumber', 'status')
