from django.urls import path, include
from api import views

urlpatterns = [
    path('resume/', views.ProfileView.as_view(), name='resume'),
    path('list/', views.ProfileView.as_view(), name='list'),
    path('auth/', include('authapi.urls')), # add this line

]