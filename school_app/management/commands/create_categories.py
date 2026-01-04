# school_app/management/commands/create_categories.py
from django.core.management.base import BaseCommand
from school_app.models import DocumentCategory

class Command(BaseCommand):
    help = 'Create initial document categories'

    def handle(self, *args, **kwargs):
        categories = [
            {
                'name': 'Academic Calendar',
                'slug': 'academic-calendar',
                'icon': 'fas fa-calendar-alt',
                'display_order': 1,
                'is_active': True
            },
            {
                'name': 'Admissions',
                'slug': 'admissions',
                'icon': 'fas fa-graduation-cap',
                'display_order': 2,
                'is_active': True
            },
            {
                'name': 'Application Forms',
                'slug': 'application-forms',
                'icon': 'fas fa-file-alt',
                'display_order': 3,
                'is_active': True
            },
            {
                'name': 'School Policies',
                'slug': 'school-policies',
                'icon': 'fas fa-gavel',
                'display_order': 4,
                'is_active': True
            },
            {
                'name': 'Exam Papers',
                'slug': 'exam-papers',
                'icon': 'fas fa-file-contract',
                'display_order': 5,
                'is_active': True
            },
            {
                'name': 'Reports',
                'slug': 'reports',
                'icon': 'fas fa-chart-bar',
                'display_order': 6,
                'is_active': True
            },
        ]

        for cat_data in categories:
            category, created = DocumentCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created category: {category.name}'))
            else:
                self.stdout.write(f'✓ Category already exists: {category.name}')