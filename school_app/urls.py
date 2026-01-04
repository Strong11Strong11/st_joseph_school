from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('news/', views.all_news, name='all_news'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    path('services/', views.services, name='services'),
    path('add-news/', views.add_news, name='add_news'),
    path('academic-calendar/', views.academic_calendar, name='academic_calendar'),
    path('admissions/', views.admissions, name='admissions'),
    path('application-form/', views.application_form, name='application_form'),
    path('documents/download/<slug:slug>/', views.download_document, name='download_document'),
    path('manage-school-info/', views.manage_school_info, name='manage_school_info'),
    
    # Document management (staff only)
    path('staff/documents/', views.manage_documents, name='manage_documents'),
    path('staff/documents/add/', views.add_document, name='add_document'),
    path('staff/documents/edit/<slug:slug>/', views.edit_document, name='edit_document'), 
    path('staff/documents/delete/<slug:slug>/', views.delete_document, name='delete_document'), 
    path('staff/documents/categories/', views.manage_categories, name='manage_categories'),
    path('staff/documents/categories/edit/<slug:slug>/', views.edit_category, name='edit_category'),
    path('staff/documents/categories/delete/<slug:slug>/', views.delete_category, name='delete_category'), 
    path('staff/documents/edit-by-uuid/<uuid:uuid>/', views.get_document_by_uuid, name='get_document_by_uuid'),
    path('staff/documents/categories/edit-by-uuid/<uuid:uuid>/', views.get_category_by_uuid, name='get_category_by_uuid'),
]