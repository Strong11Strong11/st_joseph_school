from django.contrib import admin
from .models import AboutPage, TeamMember, Facility

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1

class FacilityInline(admin.TabularInline):
    model = Facility
    extra = 1

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    inlines = [TeamMemberInline, FacilityInline]
    list_display = ('title', 'updated_at')
    
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'department', 'is_active')
    list_filter = ('position', 'is_active')
    search_fields = ('name', 'department', 'qualification')
    list_editable = ('is_active',)

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'about_page')