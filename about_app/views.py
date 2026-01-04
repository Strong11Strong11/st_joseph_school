from django.shortcuts import render, get_object_or_404
from .models import AboutPage
from school_app.models import SchoolInfo

def about_view(request):
    about_page = AboutPage.objects.first()
    school_info = SchoolInfo.objects.first()

    if not about_page:
        about_page = AboutPage.objects.create(title="About St Joseph Mission School")
    
    context = {
        'about_page': about_page,
        'team_members': about_page.team_members.filter(is_active=True),
        'facilities': about_page.facilities.all(),
        'school_info': school_info, 
    }
    return render(request, 'about/about.html', context)

def team_view(request):
    about_page = AboutPage.objects.first()
    if not about_page:
        about_page = AboutPage.objects.create(title="About St Joseph Mission School")
    
    context = {
        'about_page': about_page,
        'team_members': about_page.team_members.filter(is_active=True),
    }
    return render(request, 'about/team.html', context)