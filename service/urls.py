from django.contrib import admin
from django.urls import path, include
from .views import ServiceCreationView,ServiceListView,ServiceDetailView,ServiceDeleteView,ServiceUpdateView,UrbanCreateView
from .import views
from .views import profile

# from django.conf import settings
# from django.conf.urls.static import static
urlpatterns = [
 
 path("create/",ServiceCreationView.as_view(),name="service_create"),
 path("list/",ServiceListView.as_view(),name="service_list"),
 path("detail/<int:pk>/",ServiceDetailView.as_view(),name="detail_service"),
 path("delete/<int:pk>/",ServiceDeleteView.as_view(),name="delete_service"),
 path("update/<int:pk>/",ServiceUpdateView.as_view(),name="update_service"),
#  path ("chart/",views.pieChart,name="chart"),
path("urban_create/",UrbanCreateView.as_view(),name="urban_create"),
path("urban_list/",views.UrbanListView.as_view(),name="urban_list"),
path('profile/',profile, name='service_profile'),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)