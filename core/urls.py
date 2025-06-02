from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import MachineAPI, MaintenanceAPI, ClaimAPI, MachineViewSet, MaintenanceViewSet, ClaimViewSet
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('machines/', views.machine_list, name='machine_list'),
    path('machines/<int:pk>/', views.machine_detail, name='machine_detail'),
    path('machines/add/', views.add_machine, name='add_machine'),
    path('machines/<int:pk>/edit/', views.edit_machine, name='edit_machine'),
    path('machines/<int:pk>/delete/', views.delete_machine, name='delete_machine'),
    path('search/', views.machine_search, name='machine_search'),

    path('maintenance/', views.maintenance_list, name='maintenance_list'),
    path('maintenance/<int:pk>/', views.maintenance_detail, name='maintenance_detail'),
    path('maintenance/add/', views.add_maintenance, name='add_maintenance'),
    path('maintenance/<int:pk>/edit/', views.edit_maintenance, name='edit_maintenance'),

    path('claims/', views.claim_list, name='claim_list'),
    path('claims/<int:pk>/', views.claim_detail, name='claim_detail'),
    path('claims/add/', views.add_claim, name='add_claim'),
    path('claims/<int:pk>/edit/', views.edit_claim, name='edit_claim'),
]

urlpatterns += [
    path('api/machines/', MachineAPI.as_view(), name='api_machines'),
    path('api/maintenance/', MaintenanceAPI.as_view(), name='api_maintenance'),
    path('api/claims/', ClaimAPI.as_view(), name='api_claims'),
]

router = DefaultRouter()
router.register(r'api/machines', MachineViewSet, basename='api_machines')
router.register(r'api/maintenance', MaintenanceViewSet, basename='api_maintenance')
router.register(r'api/claims', ClaimViewSet, basename='api_claims')

urlpatterns += router.urls
