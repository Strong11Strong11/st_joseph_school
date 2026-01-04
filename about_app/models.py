from django.db import models
from django.utils import timezone

class AboutPage(models.Model):
    title = models.CharField(max_length=200, default="About St Joseph Mission School")
    history = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    values = models.TextField(blank=True, help_text="List core values separated by commas")
    achievements = models.TextField(blank=True, help_text="Notable achievements and awards")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "About Page"
    
    def __str__(self):
        return self.title

class TeamMember(models.Model):
    POSITION_CHOICES = [
        ('manager', 'Manager'),
        ('school_commitee', 'School Commitee'),
        ('teacher', 'Teacher'),
        ('headmistress', 'Headmistress'),
        ('asst_headmistress', 'Asst. Headmistress'),
        ('dean_of_discipline', 'Dean of Discipline'),
        ('academic_dean', 'Academic Dean'),
        ('environment_head', 'Environment Head'),
        ('sports_and_games_head', 'Sports & Games Head'),
        ('board', 'Board Member'),
    ]
    
    about_page = models.ForeignKey(AboutPage, related_name='team_members', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=30, choices=POSITION_CHOICES)
    department = models.CharField(max_length=100, blank=True)
    qualification = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='team_images/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    join_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'position', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.get_position_display()}"

class Facility(models.Model):
    about_page = models.ForeignKey(AboutPage, related_name='facilities', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='facility_images/', blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    
    def __str__(self):
        return self.name