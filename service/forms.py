from django import forms
from .models import Service, Urban #, ServiceTeam


class ServiceCreationForm(forms.ModelForm):
    class Meta:
        model = Service
        fields ='__all__'
        
        

# class ServiceTeamCreationForm(forms.ModelForm):
#     class Meta:
#         model = ServiceTeam
#         fields ='__all__'        
        
 
class UrbanCreationForm(forms.ModelForm):
    class Meta:
        model = Urban
        fields ='__all__'