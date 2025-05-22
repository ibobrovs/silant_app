from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('machines/', views.machine_list, name='machine_list'),
    path('machines/<int:pk>/', views.machine_detail, name='machine_detail'),

    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/<int:pk>/', views.maintenance_detail, name='maintenance_detail'),

    path('claims/', views.claim_list, name='claim_list'),
    path('claims/<int:pk>/', views.claim_detail, name='claim_detail'),
]
