from django.contrib import admin
from .models import News, SchoolInfo, DocumentCategory, DownloadableDocument

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'news_type', 'created_at', 'is_published')
    list_filter = ('news_type', 'is_published', 'created_at')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)

@admin.register(SchoolInfo)
class SchoolInfoAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Allow only one SchoolInfo instance
        if SchoolInfo.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
    
@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'display_order', 'is_active', 'document_count']
    list_editable = ['display_order', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def document_count(self, obj):
        return obj.documents.count()
    document_count.short_description = 'Documents'

@admin.register(DownloadableDocument)
class DownloadableDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'file_type', 'file_size', 'requires_login', 'download_count', 'is_active', 'created_at']  # ADDED 'requires_login' HERE
    list_filter = ['category', 'file_type', 'is_active', 'requires_login', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active', 'requires_login']  # This requires 'requires_login' to be in list_display
    readonly_fields = ['file_type', 'file_size', 'download_count', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'category')
        }),
        ('File Details', {
            'fields': ('file', 'thumbnail', 'file_type', 'file_size')
        }),
        ('Settings', {
            'fields': ('is_active', 'requires_login', 'published_date')
        }),
        ('Statistics', {
            'fields': ('download_count', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If creating new
            obj.created_by = request.user
        super().save_model(request, obj, form, change)