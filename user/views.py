from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import User, Item, Booking, Invoice
from .forms import CustomerRegistrationForm, ServiceproviderRegistrationForm, ProfileForm


# Generate PDF
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO

# Note: Ensure to import any other required models or forms.

# User Registration for Customers
class CustomerRegisterView(CreateView):
    template_name = 'user/customer_register.html'
    form_class = CustomerRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Upon successful form validation, send a welcome email.
        valid = super().form_valid(form)
        email = form.cleaned_data.get('email')
        if email:
            self.send_welcome_email(email)
        return valid

    def send_welcome_email(self, email):
        subject = 'Welcome to Our Service'
        message = 'Thank you for registering with us. We are glad to have you on board!'
        send_mail(subject, message, settings.EMAIL_HOST_USER or None, [email], fail_silently=True)

# User Registration for Service Providers
class ServiceproviderRegisterView(CreateView):
    template_name = 'user/serviceprovider_register.html'
    form_class = ServiceproviderRegistrationForm
    success_url = reverse_lazy('login')

# User Login View
class UserLoginView(LoginView):
    template_name = 'user/login.html'
    
    def get_success_url(self):
        # Redirect users based on their role after login.
        if self.request.user.is_customer:
            return reverse_lazy('customer-dashboard')
        elif self.request.user.is_serviceprovider:
            return reverse_lazy('serviceprovider-dashboard')
        else:
            return reverse_lazy('home')

# Customer Dashboard View
class CustomerDashboardView(LoginRequiredMixin, ListView):
    model = Item  # Assuming you want to list items or services
    template_name = 'user/customer_dashboard.html'
    context_object_name = 'items'
    
    def get_queryset(self):
        # Customize the queryset as per your requirements, e.g., filter available items.
        return Item.objects.filter(available=True)

# Service Provider Dashboard View
class ServiceproviderDashboardView(LoginRequiredMixin, ListView):
    template_name = 'user/serviceprovider_dashboard.html'

    def get_queryset(self):
        from service.models import Service
        return Service.objects.filter(serviceprovider=self.request.user)

# Profile Update View
class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'user/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        # Users can only edit their own profile
        return self.request.user

# Static Pages
def home(request):
    # Display home page with a list of items/services.
    items = Item.objects.all()
    return render(request, 'user/home.html', {'items': items})

def about_us(request):
    return render(request, 'user/aboutus.html')

def contact(request):
    return render(request, 'user/contact.html')

# Booking and Invoice
def book_now(request, item_id):
    if request.method == "POST" and request.user.is_authenticated:
        item = get_object_or_404(Item, id=item_id)
        booking = Booking.objects.create(user=request.user, item=item, bdate=timezone.now())
        Invoice.objects.create(booking=booking, amount=item.price, status="Pending")
        return redirect('show_invoice', invoice_id=booking.invoice.id)
    else:
        return redirect('login')


@login_required(login_url='/user/login/')
def show_invoice(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id, booking__user=request.user)
    item = invoice.booking.item
    return render(request, 'user/invoice.html', {'invoice': invoice,'item': item})

def submit(request):
    return render(request, 'user/submit.html')


def terms(request):
    return render(request, 'user/terms.html')

def payment(request):
    return render(request, 'user/payment.html')


@login_required(login_url='/user/login/')
def invoice_pdf(request, invoice_id):
    # Fetch the invoice and item objects
    invoice = get_object_or_404(Invoice, id=invoice_id, booking__user=request.user)
    item = invoice.booking.item
    
    # Create a buffer to store the PDF content
    buffer = BytesIO()
    
    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Add content to the PDF
    data = [
        ["Item Description", "Hours", "Status", "Sub-total"],
        [item.title, "2", invoice.status, str(item.price)]
    ]
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    elements.append(table)
    
    # Build the PDF document
    doc.build(elements)
    
    # Get PDF content from the buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Create a HTTP response with PDF content
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{invoice_id}.pdf"'
    return response