from django.db import models
from django.utils import timezone

class ContactInfo(models.Model):
    title = models.CharField(max_length=200, default="Contact Information")
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    fax = models.CharField(max_length=20, blank=True)
    office_hours = models.TextField(blank=True)
    map_embed_code = models.TextField(blank=True, help_text="Google Maps embed code")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Contact Information"
    
    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name_plural = "Contact Messages"
    
    def __str__(self):
        return f"{self.name} - {self.subject}"