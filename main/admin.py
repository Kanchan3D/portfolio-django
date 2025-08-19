"""
MongoDB Data Management Admin Interface
Since Django's default admin doesn't work with MongoEngine, we create custom views
"""

from django.contrib import admin
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils.html import format_html
from django.http import JsonResponse
from django.urls import path
from django.template.response import TemplateResponse
import json
from datetime import datetime, date

# Admin site customization
admin.site.site_header = "Kanchan's Portfolio - MongoDB Admin"
admin.site.site_title = "Portfolio MongoDB Admin"
admin.site.index_title = "MongoDB Content Management"

# MongoDB Admin Views (standalone functions)
@staff_member_required
def mongodb_admin_index(request):
    """Main admin dashboard with MongoDB data management"""
    try:
        from .models import Certificate, CV, Project, Profile
        
        # Get data from MongoDB
        certificates = list(Certificate.objects.all())
        projects = list(Project.objects.all())
        cvs = list(CV.objects.all())
        
        # Get active profile
        active_profile = Profile.objects(is_active=True).first()
        profile_count = Profile.objects.count()
        
        context = {
            'title': 'MongoDB Data Management',
            'certificates': certificates,
            'certificates_count': len(certificates),
            'projects': projects,
            'projects_count': len(projects),
            'cvs': cvs,
            'cvs_count': len(cvs),
            'active_profile': active_profile,
            'profile_count': profile_count,
            'has_permission': True,
            'site_title': admin.site.site_title,
            'site_header': admin.site.site_header,
            'index_title': admin.site.index_title,
        }
        
        return TemplateResponse(request, 'admin/mongodb_data_admin.html', context)
        
    except Exception as e:
        messages.error(request, f'MongoDB Error: {str(e)}')
        return TemplateResponse(request, 'admin/mongodb_error.html', {
            'error': str(e),
            'title': 'MongoDB Error',
            'has_permission': True,
            'site_title': admin.site.site_title,
            'site_header': admin.site.site_header,
        })

@staff_member_required
def delete_certificate(request, cert_id):
    """Delete a certificate"""
    try:
        from .models import Certificate
        cert = Certificate.objects(id=cert_id).first()
        if cert:
            title = cert.title
            cert.delete()
            messages.success(request, f'Certificate "{title}" deleted successfully!')
        else:
            messages.error(request, 'Certificate not found!')
    except Exception as e:
        messages.error(request, f'Error deleting certificate: {str(e)}')
    
    return redirect('admin:index')

@staff_member_required
def delete_project(request, project_id):
    """Delete a project"""
    try:
        from .models import Project
        project = Project.objects(id=project_id).first()
        if project:
            title = project.title
            project.delete()
            messages.success(request, f'Project "{title}" deleted successfully!')
        else:
            messages.error(request, 'Project not found!')
    except Exception as e:
        messages.error(request, f'Error deleting project: {str(e)}')
    
    return redirect('admin:index')

@staff_member_required
def delete_cv(request, cv_id):
    """Delete a CV"""
    try:
        from .models import CV
        cv = CV.objects(id=cv_id).first()
        if cv:
            title = cv.title
            cv.delete()
            messages.success(request, f'CV "{title}" deleted successfully!')
        else:
            messages.error(request, 'CV not found!')
    except Exception as e:
        messages.error(request, f'Error deleting CV: {str(e)}')
    
    return redirect('admin:index')

@staff_member_required
def add_sample_data(request):
    """Add sample data to MongoDB"""
    try:
        from .models import Certificate, Project, CV
        
        # Add sample certificate
        cert = Certificate(
            title=f'Sample Certificate {datetime.now().strftime("%H%M")}',
            issuer='Sample Institution',
            description='This is a sample certificate for testing',
            pdf_url='https://example.com/sample-cert.pdf',
            issue_date=date.today(),
            is_featured=True,
            display_order=999
        )
        cert.save()
        
        # Add sample project
        project = Project(
            title=f'Sample Project {datetime.now().strftime("%H%M")}',
            description='This is a sample project for testing the MongoDB admin interface',
            image_url='https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400',
            technologies='React, Node.js, MongoDB, Express',
            github_url='https://github.com/sample/repo',
            live_url='https://sample-demo.com',
            is_featured=True
        )
        project.save()
        
        messages.success(request, 'Sample certificate and project added successfully!')
        
    except Exception as e:
        messages.error(request, f'Error adding sample data: {str(e)}')
    
    return redirect('admin:index')

@staff_member_required
def add_certificate(request):
    """Add a new certificate"""
    if request.method == 'POST':
        try:
            from .models import Certificate
            
            # Get form data
            title = request.POST.get('title', '').strip()
            issuer = request.POST.get('issuer', '').strip()
            description = request.POST.get('description', '').strip()
            pdf_url = request.POST.get('pdf_url', '').strip()
            issue_date_str = request.POST.get('issue_date', '').strip()
            display_order = request.POST.get('display_order', '1')
            is_featured = request.POST.get('is_featured') == 'on'
            
            # Validate required fields
            if not title:
                return TemplateResponse(request, 'admin/certificate_form.html', {
                    'action_title': 'Add New Certificate',
                    'action_button': 'Save Certificate',
                    'error_message': 'Title is required',
                    'form_data': request.POST,
                    'site_title': admin.site.site_title,
                    'site_header': admin.site.site_header,
                })
            
            # Parse date
            issue_date = None
            if issue_date_str:
                try:
                    issue_date = datetime.strptime(issue_date_str, '%Y-%m-%d').date()
                except ValueError:
                    pass
            
            # Create certificate
            cert = Certificate(
                title=title,
                issuer=issuer if issuer else None,
                description=description if description else None,
                pdf_url=pdf_url if pdf_url else None,
                issue_date=issue_date,
                display_order=int(display_order) if display_order.isdigit() else 1,
                is_featured=is_featured
            )
            cert.save()
            
            messages.success(request, f'Certificate "{title}" added successfully!')
            return redirect('admin:index')
            
        except Exception as e:
            return TemplateResponse(request, 'admin/certificate_form.html', {
                'action_title': 'Add New Certificate',
                'action_button': 'Save Certificate',
                'error_message': f'Error saving certificate: {str(e)}',
                'form_data': request.POST,
                'site_title': admin.site.site_title,
                'site_header': admin.site.site_header,
            })
    
    # GET request - show form
    return TemplateResponse(request, 'admin/certificate_form.html', {
        'action_title': 'Add New Certificate',
        'action_button': 'Save Certificate',
        'site_title': admin.site.site_title,
        'site_header': admin.site.site_header,
    })

@staff_member_required
def edit_certificate(request, cert_id):
    """Edit an existing certificate"""
    try:
        from .models import Certificate
        cert = Certificate.objects(id=cert_id).first()
        if not cert:
            messages.error(request, 'Certificate not found!')
            return redirect('admin:index')
        
        if request.method == 'POST':
            # Update certificate
            title = request.POST.get('title', '').strip()
            issuer = request.POST.get('issuer', '').strip()
            description = request.POST.get('description', '').strip()
            pdf_url = request.POST.get('pdf_url', '').strip()
            issue_date_str = request.POST.get('issue_date', '').strip()
            display_order = request.POST.get('display_order', '1')
            is_featured = request.POST.get('is_featured') == 'on'
            
            if not title:
                return TemplateResponse(request, 'admin/certificate_form.html', {
                    'action_title': 'Edit Certificate',
                    'action_button': 'Update Certificate',
                    'error_message': 'Title is required',
                    'form_data': request.POST,
                    'site_title': admin.site.site_title,
                    'site_header': admin.site.site_header,
                })
            
            # Parse date
            issue_date = None
            if issue_date_str:
                try:
                    issue_date = datetime.strptime(issue_date_str, '%Y-%m-%d').date()
                except ValueError:
                    pass
            
            # Update fields
            cert.title = title
            cert.issuer = issuer if issuer else None
            cert.description = description if description else None
            cert.pdf_url = pdf_url if pdf_url else None
            cert.issue_date = issue_date
            cert.display_order = int(display_order) if display_order.isdigit() else 1
            cert.is_featured = is_featured
            cert.save()
            
            messages.success(request, f'Certificate "{title}" updated successfully!')
            return redirect('admin:index')
        
        # GET request - show form with existing data
        form_data = {
            'title': cert.title,
            'issuer': cert.issuer,
            'description': cert.description,
            'pdf_url': cert.pdf_url,
            'issue_date': cert.issue_date.strftime('%Y-%m-%d') if cert.issue_date else '',
            'display_order': cert.display_order,
            'is_featured': cert.is_featured,
        }
        
        return TemplateResponse(request, 'admin/certificate_form.html', {
            'action_title': 'Edit Certificate',
            'action_button': 'Update Certificate',
            'form_data': form_data,
            'site_title': admin.site.site_title,
            'site_header': admin.site.site_header,
        })
        
    except Exception as e:
        messages.error(request, f'Error editing certificate: {str(e)}')
        return redirect('admin:index')

@staff_member_required
def add_project(request):
    """Add a new project"""
    if request.method == 'POST':
        try:
            from .models import Project
            
            # Get form data
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            technologies = request.POST.get('technologies', '').strip()
            image_url = request.POST.get('image_url', '').strip()
            github_url = request.POST.get('github_url', '').strip()
            live_url = request.POST.get('live_url', '').strip()
            is_featured = request.POST.get('is_featured') == 'on'
            
            # Validate required fields
            if not title or not description:
                return TemplateResponse(request, 'admin/project_form.html', {
                    'action_title': 'Add New Project',
                    'action_button': 'Save Project',
                    'error_message': 'Title and description are required',
                    'form_data': request.POST,
                    'site_title': admin.site.site_title,
                    'site_header': admin.site.site_header,
                })
            
            # Create project
            project = Project(
                title=title,
                description=description,
                technologies=technologies if technologies else None,
                image_url=image_url if image_url else None,
                github_url=github_url if github_url else None,
                live_url=live_url if live_url else None,
                is_featured=is_featured
            )
            project.save()
            
            messages.success(request, f'Project "{title}" added successfully!')
            return redirect('admin:index')
            
        except Exception as e:
            return TemplateResponse(request, 'admin/project_form.html', {
                'action_title': 'Add New Project',
                'action_button': 'Save Project',
                'error_message': f'Error saving project: {str(e)}',
                'form_data': request.POST,
                'site_title': admin.site.site_title,
                'site_header': admin.site.site_header,
            })
    
    # GET request - show form
    return TemplateResponse(request, 'admin/project_form.html', {
        'action_title': 'Add New Project',
        'action_button': 'Save Project',
        'site_title': admin.site.site_title,
        'site_header': admin.site.site_header,
    })

@staff_member_required
def edit_project(request, project_id):
    """Edit an existing project"""
    try:
        from .models import Project
        project = Project.objects(id=project_id).first()
        if not project:
            messages.error(request, 'Project not found!')
            return redirect('admin:index')
        
        if request.method == 'POST':
            # Update project
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            technologies = request.POST.get('technologies', '').strip()
            image_url = request.POST.get('image_url', '').strip()
            github_url = request.POST.get('github_url', '').strip()
            live_url = request.POST.get('live_url', '').strip()
            is_featured = request.POST.get('is_featured') == 'on'
            
            if not title or not description:
                return TemplateResponse(request, 'admin/project_form.html', {
                    'action_title': 'Edit Project',
                    'action_button': 'Update Project',
                    'error_message': 'Title and description are required',
                    'form_data': request.POST,
                    'site_title': admin.site.site_title,
                    'site_header': admin.site.site_header,
                })
            
            # Update fields
            project.title = title
            project.description = description
            project.technologies = technologies if technologies else None
            project.image_url = image_url if image_url else None
            project.github_url = github_url if github_url else None
            project.live_url = live_url if live_url else None
            project.is_featured = is_featured
            project.save()
            
            messages.success(request, f'Project "{title}" updated successfully!')
            return redirect('admin:index')
        
        # GET request - show form with existing data
        form_data = {
            'title': project.title,
            'description': project.description,
            'technologies': project.technologies,
            'image_url': project.image_url,
            'github_url': project.github_url,
            'live_url': project.live_url,
            'is_featured': project.is_featured,
        }
        
        return TemplateResponse(request, 'admin/project_form.html', {
            'action_title': 'Edit Project',
            'action_button': 'Update Project',
            'form_data': form_data,
            'site_title': admin.site.site_title,
            'site_header': admin.site.site_header,
        })
        
    except Exception as e:
        messages.error(request, f'Error editing project: {str(e)}')
        return redirect('admin:index')

@staff_member_required
def add_cv(request):
    """Add a new CV"""
    if request.method == 'POST':
        try:
            from .models import CV
            
            # Get form data
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            pdf_url = request.POST.get('pdf_url', '').strip()
            is_current = request.POST.get('is_current') == 'on'
            
            # Validate required fields
            if not title or not pdf_url:
                return TemplateResponse(request, 'admin/cv_form.html', {
                    'action_title': 'Add New CV',
                    'action_button': 'Save CV',
                    'error_message': 'Title and PDF URL are required',
                    'form_data': request.POST,
                    'site_title': admin.site.site_title,
                    'site_header': admin.site.site_header,
                })
            
            # If marking as current, unmark others
            if is_current:
                CV.objects.update(is_current=False)
            
            # Create CV
            cv = CV(
                title=title,
                description=description if description else None,
                pdf_url=pdf_url,
                is_current=is_current
            )
            cv.save()
            
            messages.success(request, f'CV "{title}" added successfully!')
            return redirect('admin:index')
            
        except Exception as e:
            return TemplateResponse(request, 'admin/cv_form.html', {
                'action_title': 'Add New CV',
                'action_button': 'Save CV',
                'error_message': f'Error saving CV: {str(e)}',
                'form_data': request.POST,
                'site_title': admin.site.site_title,
                'site_header': admin.site.site_header,
            })
    
    # GET request - show form
    return TemplateResponse(request, 'admin/cv_form.html', {
        'action_title': 'Add New CV',
        'action_button': 'Save CV',
        'site_title': admin.site.site_title,
        'site_header': admin.site.site_header,
    })

@staff_member_required
def edit_cv(request, cv_id):
    """Edit an existing CV"""
    try:
        from .models import CV
        cv = CV.objects(id=cv_id).first()
        if not cv:
            messages.error(request, 'CV not found!')
            return redirect('admin:index')
        
        if request.method == 'POST':
            # Update CV
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            pdf_url = request.POST.get('pdf_url', '').strip()
            is_current = request.POST.get('is_current') == 'on'
            
            if not title or not pdf_url:
                return TemplateResponse(request, 'admin/cv_form.html', {
                    'action_title': 'Edit CV',
                    'action_button': 'Update CV',
                    'error_message': 'Title and PDF URL are required',
                    'form_data': request.POST,
                    'site_title': admin.site.site_title,
                    'site_header': admin.site.site_header,
                })
            
            # If marking as current, unmark others
            if is_current:
                CV.objects.update(is_current=False)
            
            # Update fields
            cv.title = title
            cv.description = description if description else None
            cv.pdf_url = pdf_url
            cv.is_current = is_current
            cv.save()
            
            messages.success(request, f'CV "{title}" updated successfully!')
            return redirect('admin:index')
        
        # GET request - show form with existing data
        form_data = {
            'title': cv.title,
            'description': cv.description,
            'pdf_url': cv.pdf_url,
            'is_current': cv.is_current,
        }
        
        return TemplateResponse(request, 'admin/cv_form.html', {
            'action_title': 'Edit CV',
            'action_button': 'Update CV',
            'form_data': form_data,
            'site_title': admin.site.site_title,
            'site_header': admin.site.site_header,
        })
        
    except Exception as e:
        messages.error(request, f'Error editing CV: {str(e)}')
        return redirect('admin:index')

@staff_member_required
def manage_profile(request):
    """Manage the single portfolio profile"""
    from django.contrib import messages
    from django.shortcuts import redirect
    from django.template.response import TemplateResponse
    from django.contrib import admin
    from .models import Profile
    
    try:
        # Always get the first (and should be only) profile
        profile = Profile.objects.first()
    except Exception as e:
        print(f"⚠️ MongoDB error getting profile: {e}")
        profile = None

    if request.method == 'POST':
        # Process form submission
        try:
            # Extract form data
            name = request.POST.get('name', '').strip()
            title = request.POST.get('title', '').strip()
            bio = request.POST.get('bio', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            location = request.POST.get('location', '').strip()
            linkedin_url = request.POST.get('linkedin_url', '').strip()
            github_url = request.POST.get('github_url', '').strip()
            twitter_url = request.POST.get('twitter_url', '').strip()
            instagram_url = request.POST.get('instagram_url', '').strip()
            website_url = request.POST.get('website_url', '').strip()
            profile_photo_url = request.POST.get('profile_photo_url', '').strip()
            resume_url = request.POST.get('resume_url', '').strip()
            years_experience = request.POST.get('years_experience', '0')
            skills = request.POST.get('skills', '').strip()
            languages = request.POST.get('languages', '').strip()
            is_available_for_work = request.POST.get('is_available_for_work') == 'on'
            
            # Validate required fields
            if not name or not email:
                action_title = 'Edit Profile' if profile else 'Create Profile'
                return TemplateResponse(request, 'admin/profile_form.html', {
                    'action_title': action_title,
                    'action_button': 'Update Profile' if profile else 'Create Profile',
                    'error_message': 'Name and email are required',
                    'form_data': request.POST,
                    'site_title': admin.site.site_title,
                    'site_header': admin.site.site_header,
                })
            
            # Update existing profile or create the first one
            if profile:
                # Update existing profile
                profile.name = name
                profile.title = title if title else None
                profile.bio = bio if bio else None
                profile.email = email
                profile.phone = phone if phone else None
                profile.location = location if location else None
                profile.linkedin_url = linkedin_url if linkedin_url else None
                profile.github_url = github_url if github_url else None
                profile.twitter_url = twitter_url if twitter_url else None
                profile.instagram_url = instagram_url if instagram_url else None
                profile.website_url = website_url if website_url else None
                profile.profile_photo_url = profile_photo_url if profile_photo_url else None
                profile.resume_url = resume_url if resume_url else None
                profile.years_experience = int(years_experience) if years_experience.isdigit() else 0
                profile.skills = skills if skills else None
                profile.languages = languages if languages else None
                profile.is_active = True  # Always set to active since there's only one profile
                profile.is_available_for_work = is_available_for_work
                profile.save()
                messages.success(request, f'Profile updated successfully!')
            else:
                # Create the first and only profile
                profile = Profile(
                    name=name,
                    title=title if title else None,
                    bio=bio if bio else None,
                    email=email,
                    phone=phone if phone else None,
                    location=location if location else None,
                    linkedin_url=linkedin_url if linkedin_url else None,
                    github_url=github_url if github_url else None,
                    twitter_url=twitter_url if twitter_url else None,
                    instagram_url=instagram_url if instagram_url else None,
                    website_url=website_url if website_url else None,
                    profile_photo_url=profile_photo_url if profile_photo_url else None,
                    resume_url=resume_url if resume_url else None,
                    years_experience=int(years_experience) if years_experience.isdigit() else 0,
                    skills=skills if skills else None,
                    languages=languages if languages else None,
                    is_active=True,  # Always active since there's only one profile
                    is_available_for_work=is_available_for_work
                )
                profile.save()
                messages.success(request, f'Profile created successfully!')
            
            return redirect('admin:index')
            
        except Exception as e:
            action_title = 'Edit Profile' if profile else 'Create Profile'
            return TemplateResponse(request, 'admin/profile_form.html', {
                'action_title': action_title,
                'action_button': 'Update Profile' if profile else 'Create Profile',
                'error_message': f'Error saving profile: {str(e)}',
                'form_data': request.POST,
                'site_title': admin.site.site_title,
                'site_header': admin.site.site_header,
            })
    
    # GET request - show form with existing data or empty form
    if profile:
        form_data = {
            'name': profile.name,
            'title': profile.title,
            'bio': profile.bio,
            'email': profile.email,
            'phone': profile.phone,
            'location': profile.location,
            'linkedin_url': profile.linkedin_url,
            'github_url': profile.github_url,
            'twitter_url': profile.twitter_url,
            'instagram_url': profile.instagram_url,
            'website_url': profile.website_url,
            'profile_photo_url': profile.profile_photo_url,
            'resume_url': profile.resume_url,
            'years_experience': profile.years_experience,
            'skills': profile.skills,
            'languages': profile.languages,
            'is_active': profile.is_active,
            'is_available_for_work': profile.is_available_for_work,
        }
        action_title = 'Edit Profile'
        action_button = 'Update Profile'
    else:
        form_data = {}
        action_title = 'Create Profile'
        action_button = 'Create Profile'
    
    return TemplateResponse(request, 'admin/profile_form.html', {
        'action_title': action_title,
        'action_button': action_button,
        'form_data': form_data,
        'site_title': admin.site.site_title,
        'site_header': admin.site.site_header,
    })

# Override the default admin index
admin.site.index = mongodb_admin_index

# Register custom URLs
original_get_urls = admin.site.get_urls

def get_custom_urls():
    custom_urls = [
        # Delete URLs
        path('delete-certificate/<str:cert_id>/', delete_certificate, name='delete_certificate'),
        path('delete-project/<str:project_id>/', delete_project, name='delete_project'),
        path('delete-cv/<str:cv_id>/', delete_cv, name='delete_cv'),
        
        # Add URLs
        path('add-certificate/', add_certificate, name='add_certificate'),
        path('add-project/', add_project, name='add_project'),
        path('add-cv/', add_cv, name='add_cv'),
        path('add-sample-data/', add_sample_data, name='add_sample_data'),
        
        # Edit URLs
        path('edit-certificate/<str:cert_id>/', edit_certificate, name='edit_certificate'),
        path('edit-project/<str:project_id>/', edit_project, name='edit_project'),
        path('edit-cv/<str:cv_id>/', edit_cv, name='edit_cv'),
        
        # Profile management
        path('manage-profile/', manage_profile, name='manage_profile'),
    ]
    return custom_urls + original_get_urls()

admin.site.get_urls = get_custom_urls
