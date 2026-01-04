from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactInfo
from .forms import ContactForm
from school_app.models import SchoolInfo

def contact_view(request):
    contact_info = ContactInfo.objects.first()
    school_info = SchoolInfo.objects.first()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'contact_info': contact_info,
        'form': form,
        'school_info': school_info, 
    }
    return render(request, 'contact/contact.html', context)

def contact_success(request):
    return render(request, 'contact/success.html')