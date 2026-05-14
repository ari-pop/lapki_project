from django.contrib.auth import views as auth_views
from django.urls import path

from .forms import ShelterAuthenticationForm
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/', views.account_home, name='account_home'),
    path('register/', views.register, name='register'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='shelter/login.html',
            authentication_form=ShelterAuthenticationForm,
            redirect_authenticated_user=True,
            next_page='dashboard',
        ),
        name='login',
    ),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/admin/users/', views.admin_user_list, name='admin_user_list'),
    path('dashboard/admin/pets/', views.admin_pet_list, name='admin_pet_list'),
    path('dashboard/admin/pets/excel/', views.admin_pet_excel, name='admin_pet_excel'),
    path('dashboard/admin/pets/excel/template/', views.admin_pet_template_excel, name='admin_pet_template_excel'),
    path('dashboard/admin/pets/excel/export/', views.admin_pet_export_excel, name='admin_pet_export_excel'),
    path('dashboard/admin/pets/excel/import/', views.admin_pet_import_excel, name='admin_pet_import_excel'),
    path('dashboard/admin/pets/new/', views.admin_pet_create, name='admin_pet_create'),
    path('dashboard/admin/pets/<int:pk>/edit/', views.admin_pet_edit, name='admin_pet_edit'),
    path('dashboard/admin/news/', views.admin_news_list, name='admin_news_list'),
    path('dashboard/admin/news/new/', views.admin_news_create, name='admin_news_create'),
    path('dashboard/admin/news/<int:pk>/edit/', views.admin_news_edit, name='admin_news_edit'),
    path('dashboard/admin/applications/', views.admin_application_list, name='admin_application_list'),
    path('dashboard/admin/applications/<int:pk>/edit/', views.admin_application_edit, name='admin_application_edit'),
    path('dashboard/admin/feedback/', views.admin_feedback_list, name='admin_feedback_list'),
    path('about/', views.about, name='about'),
    path('help/', views.help_page, name='help'),
    path('contacts/', views.contacts, name='contacts'),
    path('pets/', views.pets_view, name='pets'),
    path('news/', views.news_list, name='news'),
    path('news/<int:pk>/', views.news_detail, name='news_detail'),
    path('adopt/<int:pet_id>/', views.adoption_application, name='adoption_application'),
    path('questionnaire/', views.owner_questionnaire, name='owner_questionnaire'),
]
