# migrate_from_backup.py
import sqlite3
import uuid
import os
from django.utils.text import slugify
import django

# Setup Django with NEW models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'st_joseph_school.settings')
django.setup()

from school_app.models import News, SchoolInfo, DocumentCategory, DownloadableDocument
from django.contrib.auth.models import User

def migrate_from_backup():
    print("Migrating data from backup database...")
    
    # Connect to backup database
    conn = sqlite3.connect('db.sqlite3.backup')
    cursor = conn.cursor()
    
    # Clear existing data in new database
    News.objects.all().delete()
    SchoolInfo.objects.all().delete()
    DocumentCategory.objects.all().delete()
    DownloadableDocument.objects.all().delete()
    
    # Migrate users
    print("\n1. Migrating users...")
    cursor.execute("SELECT * FROM auth_user")
    users = cursor.fetchall()
    for user_data in users:
        user_id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined = user_data
        
        # Check if user exists
        if not User.objects.filter(username=username).exists():
            user = User(
                id=user_id,  # Keep original ID for relationships
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_staff=bool(is_staff),
                is_superuser=bool(is_superuser),
                is_active=bool(is_active),
                date_joined=date_joined
            )
            user.set_password(password)
            user.save()
            print(f"  ✓ User: {username}")
    
    # Migrate school info
    print("\n2. Migrating school info...")
    cursor.execute("SELECT * FROM school_app_schoolinfo")
    school_info_data = cursor.fetchall()
    for info in school_info_data:
        info_id, name, motto, address, phone, email, principal_name, principal_message = info
        
        SchoolInfo.objects.create(
            id=uuid.uuid4(),
            name=name or "St Joseph Mission School",
            motto=motto or "",
            address=address or "",
            phone=phone or "",
            email=email or "",
            principal_name=principal_name or "",
            principal_message=principal_message or ""
        )
        print(f"  ✓ School Info")
    
    # Migrate categories
    print("\n3. Migrating categories...")
    cursor.execute("SELECT * FROM school_app_documentcategory")
    categories = cursor.fetchall()
    
    category_map = {}  # Map old ID to new object
    
    for cat in categories:
        cat_id, name, description, icon, display_order, is_active = cat
        
        # Create UUID and slug
        cat_uuid = uuid.uuid4()
        base_slug = slugify(name)
        slug = f"{base_slug}-{str(cat_uuid)[:8]}"
        
        # Ensure unique slug
        counter = 1
        original_slug = slug
        while DocumentCategory.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        category = DocumentCategory.objects.create(
            id=cat_uuid,
            name=name,
            slug=slug,
            description=description or "",
            icon=icon or "fas fa-file",
            display_order=display_order or 0,
            is_active=bool(is_active) if is_active is not None else True
        )
        category_map[cat_id] = category
        print(f"  ✓ Category: {name}")
    
    # Migrate documents
    print("\n4. Migrating documents...")
    cursor.execute("SELECT * FROM school_app_downloadabledocument")
    documents = cursor.fetchall()
    
    for doc in documents:
        (doc_id, title, description, category_id, file_path, file_type, 
         file_size, thumbnail, download_count, is_active, requires_login, 
         created_by_id, created_at, updated_at, published_date) = doc
        
        # Get category
        category = category_map.get(category_id)
        if not category:
            print(f"  ⚠ Skipping document '{title}' - category ID {category_id} not found")
            continue
        
        # Get user
        try:
            user = User.objects.get(id=created_by_id)
        except User.DoesNotExist:
            user = User.objects.first()
        
        # Create UUID and slug
        doc_uuid = uuid.uuid4()
        base_slug = slugify(title)
        slug = f"{base_slug}-{str(doc_uuid)[:8]}"
        
        # Ensure unique slug
        counter = 1
        original_slug = slug
        while DownloadableDocument.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        document = DownloadableDocument.objects.create(
            id=doc_uuid,
            title=title,
            slug=slug,
            description=description or "",
            category=category,
            file=file_path,
            file_type=file_type or "",
            file_size=file_size or "",
            thumbnail=thumbnail or "",
            download_count=download_count or 0,
            is_active=bool(is_active) if is_active is not None else True,
            requires_login=bool(requires_login) if requires_login is not None else False,
            created_by=user,
            published_date=published_date
        )
        print(f"  ✓ Document: {title}")
    
    # Migrate news
    print("\n5. Migrating news...")
    cursor.execute("SELECT * FROM school_app_news")
    news_items = cursor.fetchall()
    
    for news in news_items:
        (news_id, title, content, news_type, image, created_by_id, 
         created_at, updated_at, is_published) = news
        
        # Get user
        try:
            user = User.objects.get(id=created_by_id)
        except User.DoesNotExist:
            user = User.objects.first()
        
        # Create UUID and slug
        news_uuid = uuid.uuid4()
        base_slug = slugify(title)
        slug = f"{base_slug}-{str(news_uuid)[:8]}"
        
        # Ensure unique slug
        counter = 1
        original_slug = slug
        while News.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
        
        news_obj = News.objects.create(
            id=news_uuid,
            title=title,
            content=content,
            news_type=news_type or "general",
            image=image or "",
            created_by=user,
            created_at=created_at,
            updated_at=updated_at,
            is_published=bool(is_published) if is_published is not None else True,
            slug=slug
        )
        print(f"  ✓ News: {title}")
    
    conn.close()
    
    print("\n" + "=" * 50)
    print("Migration complete!")
    print(f"  Users: {User.objects.count()}")
    print(f"  School Info: {SchoolInfo.objects.count()}")
    print(f"  Categories: {DocumentCategory.objects.count()}")
    print(f"  Documents: {DownloadableDocument.objects.count()}")
    print(f"  News: {News.objects.count()}")

if __name__ == '__main__':
    migrate_from_backup()