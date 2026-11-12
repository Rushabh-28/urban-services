from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView
from .forms import ServiceCreationForm,UrbanCreationForm
from .models import Service ,Urban
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# from .models import Subcategory
# from django.conf import settings
# from .models import *
# from .forms import *

# ...


@method_decorator([login_required(login_url="/user/login")], name='dispatch')
class ServiceCreationView(CreateView):
    template_name = 'service/create.html'
    model = Service
    form_class = ServiceCreationForm
    success_url = '/service/list/'
    
    

class ServiceListView(ListView):
    template_name = 'service/list.html'
    model = Service 
    context_object_name = 'services'
    
    # def get(self, request, *args, **kwargs):
    #     serviceprovider = request.user
    #     print(serviceprovider)
    #     list_1 = Service.objects.filter(serviceprovider=serviceprovider).values()
    #     list_2 = Service.objects.filter(serviceprovider=serviceprovider).values('name','service_name','cat','subcategory','type','fees_amount','area','city','state')
    #     print(list_2)
    #     return render(request,"service/list.html",{'list_2':list_2,'list_1':list_1})
    
class ServiceDetailView(DetailView):
    model = Service
    context_object_name = "service"
    template_name = "service/service_detail.html"

@method_decorator([login_required(login_url="/user/login/")], name='dispatch')
class ServiceDeleteView(DeleteView):
    model = Service
    template_name = "service/service_delete.html"    
    success_url = "/service/list/"

    
@method_decorator([login_required(login_url="/user/login/")], name='dispatch')
class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceCreationForm
    success_url = "/service/list/"
    template_name = "service/service_update_form.html"    
    
    



@method_decorator([login_required(login_url="/user/login/")], name='dispatch')
class UrbanCreateView(CreateView):
    model = Urban
    template_name = 'service/create_urban.html'
    success_url = '/service/list/'
    form_class = UrbanCreationForm

   
class UrbanListView(ListView):
    template_name = 'service/urban_list.html'
    model = Urban
    context_object_name = 'urban'        
    
def profile(request):
    return render(request, 'service/profile.html')

