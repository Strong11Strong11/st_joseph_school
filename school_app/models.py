import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify

class News(models.Model):
    NEWS_TYPES = [
        ('announcement', 'Announcement'),
        ('event', 'Event'),
        ('achievement', 'Achievement'),
        ('general', 'General News'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    news_type = models.CharField(max_length=20, choices=NEWS_TYPES, default='general')
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    
    class Meta:
        verbose_name_plural = "News"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Create a unique slug with UUID portion to avoid conflicts
            base_slug = slugify(self.title)
            uuid_portion = str(self.id)[:8]  # Use first 8 chars of UUID
            self.slug = f"{base_slug}-{uuid_portion}"
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('news_detail', kwargs={'slug': self.slug})

class SchoolInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, default="St Joseph Mission School")
    motto = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    principal_name = models.CharField(max_length=100, blank=True)
    principal_message = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class DocumentCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-file')
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "Document Categories"
        ordering = ['display_order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Create a unique slug with UUID portion
            base_slug = slugify(self.name)
            uuid_portion = str(self.id)[:8]
            self.slug = f"{base_slug}-{uuid_portion}"
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('edit_category', kwargs={'slug': self.slug})

class DownloadableDocument(models.Model):
    DOCUMENT_TYPES = [
        ('pdf', 'PDF Document'),
        ('doc', 'Word Document'),
        ('docx', 'Word Document (DOCX)'),
        ('xls', 'Excel Spreadsheet'),
        ('xlsx', 'Excel Spreadsheet (XLSX)'),
        ('zip', 'ZIP Archive'),
        ('jpg', 'JPEG Image'),
        ('png', 'PNG Image'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE, related_name='documents')
    
    file = models.FileField(
        upload_to='documents/%Y/%m/%d/',
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'zip', 'jpg', 'jpeg', 'png'])
        ]
    )
    
    file_type = models.CharField(max_length=10, choices=DOCUMENT_TYPES, blank=True)
    file_size = models.CharField(max_length=20, blank=True)
    thumbnail = models.ImageField(upload_to='document_thumbnails/', blank=True, null=True)
    
    download_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    requires_login = models.BooleanField(default=False, help_text="Require user login to download")
    
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='uploaded_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ['-published_date', 'title']
        verbose_name = "Downloadable Document"
        verbose_name_plural = "Downloadable Documents"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Generate slug if not provided
        if not self.slug:
            base_slug = slugify(self.title)
            uuid_portion = str(self.id)[:8]
            self.slug = f"{base_slug}-{uuid_portion}"
        
        # Set file type based on extension
        if self.file:
            import os
            ext = os.path.splitext(self.file.name)[1].lower().replace('.', '')
            for file_type, name in self.DOCUMENT_TYPES:
                if ext == file_type or (ext == 'jpeg' and file_type == 'jpg'):
                    self.file_type = file_type
                    break
            
            # Calculate file size
            try:
                size = self.file.size
                if size < 1024:
                    self.file_size = f"{size} B"
                elif size < 1024 * 1024:
                    self.file_size = f"{size/1024:.1f} KB"
                else:
                    self.file_size = f"{size/(1024*1024):.1f} MB"
            except:
                pass
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('download_document', kwargs={'slug': self.slug})
    
    def get_icon_class(self):
        icon_map = {
            'pdf': 'fas fa-file-pdf text-danger',
            'doc': 'fas fa-file-word text-primary',
            'docx': 'fas fa-file-word text-primary',
            'xls': 'fas fa-file-excel text-success',
            'xlsx': 'fas fa-file-excel text-success',
            'zip': 'fas fa-file-archive text-warning',
            'jpg': 'fas fa-file-image text-info',
            'png': 'fas fa-file-image text-info',
        }
        return icon_map.get(self.file_type, 'fas fa-file')
    
    def increment_download_count(self):
        self.download_count += 1
        self.save(update_fields=['download_count'])