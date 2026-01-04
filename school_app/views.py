from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import News, SchoolInfo, DocumentCategory, DownloadableDocument
from .forms import NewsForm, SchoolInfoForm, DocumentCategoryForm, DocumentUploadForm
from django.contrib import messages
from django.http import FileResponse, Http404, JsonResponse
from django.utils.text import slugify
from django.conf import settings
import os


def home(request):
    latest_news = News.objects.filter(is_published=True).order_by('-created_at')[:7]
    school_info = SchoolInfo.objects.first()
    
    context = {
        'latest_news': latest_news,
        'school_info': school_info,
    }
    return render(request, 'school_app/home.html', context)

def services(request):
    context = {
        'page_title': 'Our Services',
        'active_page': 'services',
    }
    return render(request, 'school_app/service.html', context)

def all_news(request):
    news_items = News.objects.filter(is_published=True).order_by('-created_at')
    school_info = SchoolInfo.objects.first()

    # Filter by type if specified
    news_type = request.GET.get('type')
    if news_type:
        news_items = news_items.filter(news_type=news_type)
    
    context = {
        'news_items': news_items,
        'current_type': news_type,
        'school_info': school_info,
    }
    return render(request, 'school_app/all_news.html', context)

def news_detail(request, slug): 
    news_item = get_object_or_404(News, slug=slug, is_published=True)
    school_info = SchoolInfo.objects.first()
    
    context = {
        'news': news_item,
        'school_info': school_info,
    }
    return render(request, 'school_app/news_detail.html', context)

# Staff/Admin views
def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.created_by = request.user
            news.save()
            messages.success(request, 'News added successfully!')
            return redirect('home')
    else:
        form = NewsForm()
    
    return render(request, 'school_app/add_news.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def manage_school_info(request):
    school_info = SchoolInfo.objects.first()
    if not school_info:
        school_info = SchoolInfo()
    
    if request.method == 'POST':
        form = SchoolInfoForm(request.POST, instance=school_info)
        if form.is_valid():
            form.save()
            messages.success(request, 'School information updated!')
            return redirect('home')
    else:
        form = SchoolInfoForm(instance=school_info)
    
    return render(request, 'school_app/manage_school_info.html', {'form': form})

# Helper function to check if user is staff
def is_staff_user(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_staff_user)
def manage_documents(request):
    categories = DocumentCategory.objects.all().prefetch_related('documents')
    context = {
        'title': 'Manage Documents',
        'categories': categories,
        'documents': DownloadableDocument.objects.all(),
    }
    return render(request, 'documents/manage_documents.html', context)

@login_required
@user_passes_test(is_staff_user)
def add_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.created_by = request.user
            document.save()
            messages.success(request, f'Document "{document.title}" has been uploaded successfully!')
            return redirect('manage_documents')
    else:
        form = DocumentUploadForm()
    
    context = {
        'title': 'Upload New Document',
        'form': form,
    }
    return render(request, 'documents/add_document.html', context)

@login_required
@user_passes_test(is_staff_user)
def edit_document(request, slug): 
    document = get_object_or_404(DownloadableDocument, slug=slug)
    
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, f'Document "{document.title}" has been updated successfully!')
            return redirect('manage_documents')
    else:
        form = DocumentUploadForm(instance=document)
    
    context = {
        'title': f'Edit Document: {document.title}',
        'form': form,
        'document': document,
    }
    return render(request, 'documents/edit_document.html', context)

@login_required
@user_passes_test(is_staff_user)
def delete_document(request, slug): 
    document = get_object_or_404(DownloadableDocument, slug=slug)
    
    if request.method == 'POST':
        title = document.title
        document.delete()
        messages.success(request, f'Document "{title}" has been deleted successfully!')
        return redirect('manage_documents')
    
    context = {
        'title': 'Confirm Delete',
        'document': document,
    }
    return render(request, 'documents/confirm_delete.html', context)

@login_required
@user_passes_test(is_staff_user)
def manage_categories(request):
    categories = DocumentCategory.objects.all()
    
    if request.method == 'POST':
        form = DocumentCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" has been created!')
            return redirect('manage_categories')
    else:
        form = DocumentCategoryForm()
    
    context = {
        'title': 'Manage Document Categories',
        'categories': categories,
        'form': form,
    }
    return render(request, 'documents/manage_categories.html', context)

@login_required
@user_passes_test(is_staff_user)
def edit_category(request, slug): 
    category = get_object_or_404(DocumentCategory, slug=slug)
    
    if request.method == 'POST':
        form = DocumentCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category "{category.name}" has been updated!')
            return redirect('manage_categories')
    else:
        form = DocumentCategoryForm(instance=category)
    
    context = {
        'title': f'Edit Category: {category.name}',
        'form': form,
        'category': category,
    }
    return render(request, 'documents/edit_category.html', context)

@login_required
@user_passes_test(is_staff_user)
def delete_category(request, slug): 
    print(f"Delete category view called with slug={slug}")
    print(f"Request method: {request.method}")
    
    if request.method == 'POST':
        try:
            category = get_object_or_404(DocumentCategory, slug=slug)
            print(f"Found category: {category.name}")
            
            # Check if category has documents
            if category.documents.exists():
                print(f"Category has {category.documents.count()} documents, cannot delete")
                messages.error(request, f'Cannot delete category "{category.name}" because it contains {category.documents.count()} document(s).')
            else:
                name = category.name
                category.delete()
                print(f"Category deleted: {name}")
                messages.success(request, f'Category "{name}" has been deleted successfully!')
            
            return redirect('manage_categories')
            
        except Exception as e:
            print(f"Error deleting category: {str(e)}")
            messages.error(request, f'Error deleting category: {str(e)}')
            return redirect('manage_categories')
    
    # If GET request (shouldn't happen with modal, but just in case)
    print("GET request to delete_category - redirecting")
    return redirect('manage_categories')

# Update your existing views to use the database models
def academic_calendar(request):
    # Try to get the category by slug, create if not exists
    category, created = DocumentCategory.objects.get_or_create(
        slug='academic-calendar',
        defaults={
            'name': 'Academic Calendar',
            'icon': 'fas fa-calendar-alt',
            'display_order': 1,
            'is_active': True
        }
    )
    documents = category.documents.filter(is_active=True)
    
    context = {
        'title': 'Academic Calendar',
        'description': 'Download the current academic calendar for St. Joseph Mission School',
        'category': category,
        'documents': documents,
    }
    return render(request, 'documents/academic_calendar.html', context)

def admissions(request):
    # Try to get the category by slug, create if not exists
    category, created = DocumentCategory.objects.get_or_create(
        slug='admissions',
        defaults={
            'name': 'Admissions',
            'icon': 'fas fa-graduation-cap',
            'display_order': 2,
            'is_active': True
        }
    )
    documents = category.documents.filter(is_active=True)
    
    context = {
        'title': 'Admissions',
        'description': 'Admission information and requirements for St. Joseph Mission School',
        'category': category,
        'documents': documents,
        'sections': [
            {
                'title': 'Admission Requirements',
                'content': '''
                <ul>
                    <li>Completed application form</li>
                    <li>Birth certificate (copy)</li>
                    <li>Previous school reports (last two years)</li>
                    <li>Passport size photographs (4 copies)</li>
                    <li>Transfer letter (for transfer students)</li>
                    <li>Medical report from recognized hospital</li>
                </ul>
                '''
            },
        ]
    }
    return render(request, 'documents/admissions.html', context)

def application_form(request):
    # Try to get the category by slug, create if not exists
    category, created = DocumentCategory.objects.get_or_create(
        slug='application-forms',
        defaults={
            'name': 'Application Forms',
            'icon': 'fas fa-file-alt',
            'display_order': 3,
            'is_active': True
        }
    )
    documents = category.documents.filter(is_active=True)
    
    context = {
        'title': 'Application Forms',
        'description': 'Download and submit application forms for admission to St. Joseph Mission School',
        'category': category,
        'documents': documents,
        'instructions': [
            'Download the appropriate application form',
            'Print and fill out completely',
            'Attach all required documents',
            'Submit to the school office or email to admissions@stjosephmission.edu',
            'Allow 5-7 working days for processing'
        ]
    }
    return render(request, 'documents/application_form.html', context)

# Document download view
def download_document(request, slug):
    document = get_object_or_404(DownloadableDocument, slug=slug, is_active=True)
    
    # Check if login is required
    if document.requires_login and not request.user.is_authenticated:
        messages.error(request, 'Please login to download this document.')
        return redirect('login') + f'?next={request.path}'
    
    # Increment download count
    document.increment_download_count()
    
    # Serve the file
    response = FileResponse(document.file.open('rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename="{document.file.name.split("/")[-1]}"'
    
    return response

# Utility view to get document by UUID (for backward compatibility if needed)
@login_required
@user_passes_test(is_staff_user)
def get_document_by_uuid(request, uuid):
    """Get document by UUID and redirect to slug URL for backward compatibility"""
    try:
        document = get_object_or_404(DownloadableDocument, id=uuid)
        return redirect('edit_document', slug=document.slug)
    except:
        raise Http404("Document not found")

# Utility view to get category by UUID (for backward compatibility if needed)
@login_required
@user_passes_test(is_staff_user)
def get_category_by_uuid(request, uuid):
    """Get category by UUID and redirect to slug URL for backward compatibility"""
    try:
        category = get_object_or_404(DocumentCategory, id=uuid)
        return redirect('edit_category', slug=category.slug)
    except:
        raise Http404("Category not found")