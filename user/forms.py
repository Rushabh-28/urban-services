from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User

class CustomerRegistrationForm(UserCreationForm):
    """
    Form for registering a new customer. Inherits from UserCreationForm to utilize
    Django's built-in functionalities for user creation while adding a phone field.
    """
    phone = forms.CharField(max_length=15, required=True, help_text='Required. Add a valid phone number.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone']

    @transaction.atomic
    def save(self, commit=True):
        """
        Override the save method to ensure the user is marked as a customer
        and to save the phone number.
        """
        user = super().save(commit=False)
        user.is_customer = True
        user.phone = self.cleaned_data.get('phone')
        if commit:
            user.save()
        return user

class ServiceproviderRegistrationForm(UserCreationForm):
    """
    Form for registering a new service provider. Similar to the customer registration form
    but sets the user as a service provider.
    """
    phone = forms.CharField(max_length=15, required=True, help_text='Required. Add a valid phone number.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'phone']

    @transaction.atomic
    def save(self, commit=True):
        """
        Override the save method to ensure the user is marked as a service provider
        and to save the phone number.
        """
        user = super().save(commit=False)
        user.is_serviceprovider = True
        user.phone = self.cleaned_data.get('phone')
        if commit:
            user.save()
        return user    

class ProfileForm(forms.ModelForm):
    """
    Form for updating a user's profile. Allows users to update their email,
    first name, and last name.
    """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone']

    def __init__(self, *args, **kwargs):
        """
        Initializes the form with the user's current information.
        """
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.first_name
        self.fields['last_name'].initial = self.instance.last_name
        self.fields['email'].initial = self.instance.email

    def save(self, commit=True):
        """
        Saves the updated profile information. Updates the user's email,
        first name, and last name along with any changed phone number.
        """
        user = self.instance
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            self.instance.save()
        return self.instance


