from django import forms
from django.core.validators import FileExtensionValidator
from .models import News, SchoolInfo, DocumentCategory, DownloadableDocument

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'news_type', 'image', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SchoolInfoForm(forms.ModelForm):
    class Meta:
        model = SchoolInfo
        fields = '__all__'
        widgets = {
            'motto': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'principal_message': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }

class DocumentCategoryForm(forms.ModelForm):
    class Meta:
        model = DocumentCategory
        fields = ['name', 'description', 'icon', 'display_order', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'icon': forms.TextInput(attrs={
                'placeholder': 'e.g., fas fa-calendar, fas fa-file-pdf'
            })
        }

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = DownloadableDocument
        fields = [
            'title', 'description', 'category', 'file',
            'thumbnail', 'requires_login', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = DocumentCategory.objects.filter(is_active=True)
