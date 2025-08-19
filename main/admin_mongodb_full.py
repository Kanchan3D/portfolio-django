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

class MongoDBDataAdmin:
    """Custom admin interface for MongoDB data"""
    
    @staff_member_required
    def admin_index(self, request):
        """Main admin dashboard with MongoDB data management"""
        try:
            from .models import Certificate, CV, Project
            
            # Get data from MongoDB
            certificates = list(Certificate.objects.all())
            projects = list(Project.objects.all())
            cvs = list(CV.objects.all())
            
            context = {
                'title': 'MongoDB Data Management',
                'certificates': certificates,
                'certificates_count': len(certificates),
                'projects': projects,
                'projects_count': len(projects),
                'cvs': cvs,
                'cvs_count': len(cvs),
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
    def delete_certificate(self, request, cert_id):
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
    def delete_project(self, request, project_id):
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
    def delete_cv(self, request, cv_id):
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
    def add_sample_data(self, request):
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

# Create instance of MongoDB admin
mongodb_admin = MongoDBDataAdmin()

# Override the default admin index
admin.site.index = mongodb_admin.admin_index

# Register custom URLs
original_get_urls = admin.site.get_urls

def get_custom_urls():
    custom_urls = [
        path('delete-certificate/<str:cert_id>/', mongodb_admin.delete_certificate, name='delete_certificate'),
        path('delete-project/<str:project_id>/', mongodb_admin.delete_project, name='delete_project'),
        path('delete-cv/<str:cv_id>/', mongodb_admin.delete_cv, name='delete_cv'),
        path('add-sample-data/', mongodb_admin.add_sample_data, name='add_sample_data'),
    ]
    return custom_urls + original_get_urls()

admin.site.get_urls = get_custom_urls
