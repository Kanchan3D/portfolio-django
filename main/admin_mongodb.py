"""
MongoDB Admin Interface for Portfolio
Since Django admin doesn't work directly with MongoEngine,
we'll create a simple admin interface for MongoDB models.
"""

from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Certificate, CV, Project
import json
from datetime import datetime

@staff_member_required
def mongodb_admin_dashboard(request):
    """Main admin dashboard for MongoDB models"""
    try:
        certificates_count = Certificate.objects.count()
        projects_count = Project.objects.count()
        cvs_count = CV.objects.count()
        
        context = {
            'title': 'MongoDB Admin Dashboard',
            'certificates_count': certificates_count,
            'projects_count': projects_count,
            'cvs_count': cvs_count,
        }
        return render(request, 'admin/mongodb_dashboard.html', context)
    except Exception as e:
        messages.error(request, f'Error connecting to MongoDB: {str(e)}')
        return render(request, 'admin/mongodb_dashboard.html', {
            'title': 'MongoDB Admin Dashboard',
            'error': str(e)
        })

@staff_member_required
def certificate_list(request):
    """List all certificates"""
    try:
        certificates = Certificate.objects.all()
        context = {
            'title': 'Certificates',
            'certificates': certificates,
        }
        return render(request, 'admin/certificate_list.html', context)
    except Exception as e:
        messages.error(request, f'Error fetching certificates: {str(e)}')
        return render(request, 'admin/certificate_list.html', {'error': str(e)})

@staff_member_required
def certificate_add(request):
    """Add new certificate"""
    if request.method == 'POST':
        try:
            cert = Certificate(
                title=request.POST.get('title'),
                issuer=request.POST.get('issuer'),
                description=request.POST.get('description'),
                pdf_url=request.POST.get('pdf_url'),
                image_url=request.POST.get('image_url', ''),
                issue_date=datetime.strptime(request.POST.get('issue_date'), '%Y-%m-%d').date(),
                is_featured=request.POST.get('is_featured') == 'on',
                display_order=int(request.POST.get('display_order', 0))
            )
            cert.save()
            messages.success(request, 'Certificate added successfully!')
            return redirect('mongodb_admin:certificate_list')
        except Exception as e:
            messages.error(request, f'Error adding certificate: {str(e)}')
    
    return render(request, 'admin/certificate_form.html', {'title': 'Add Certificate'})

@staff_member_required
def project_list(request):
    """List all projects"""
    try:
        projects = Project.objects.all()
        context = {
            'title': 'Projects',
            'projects': projects,
        }
        return render(request, 'admin/project_list.html', context)
    except Exception as e:
        messages.error(request, f'Error fetching projects: {str(e)}')
        return render(request, 'admin/project_list.html', {'error': str(e)})

@staff_member_required
def project_add(request):
    """Add new project"""
    if request.method == 'POST':
        try:
            project = Project(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                image_url=request.POST.get('image_url', ''),
                technologies=request.POST.get('technologies'),
                github_url=request.POST.get('github_url', ''),
                live_url=request.POST.get('live_url', ''),
                is_featured=request.POST.get('is_featured') == 'on'
            )
            project.save()
            messages.success(request, 'Project added successfully!')
            return redirect('mongodb_admin:project_list')
        except Exception as e:
            messages.error(request, f'Error adding project: {str(e)}')
    
    return render(request, 'admin/project_form.html', {'title': 'Add Project'})

@staff_member_required
def cv_list(request):
    """List all CVs"""
    try:
        cvs = CV.objects.all()
        context = {
            'title': 'CV/Resume',
            'cvs': cvs,
        }
        return render(request, 'admin/cv_list.html', context)
    except Exception as e:
        messages.error(request, f'Error fetching CVs: {str(e)}')
        return render(request, 'admin/cv_list.html', {'error': str(e)})

@staff_member_required
def cv_add(request):
    """Add new CV"""
    if request.method == 'POST':
        try:
            # Set all other CVs to inactive
            CV.objects.update(is_active=False)
            
            cv = CV(
                title=request.POST.get('title'),
                pdf_url=request.POST.get('pdf_url'),
                version=request.POST.get('version'),
                is_active=True,  # New CV is always active
                description=request.POST.get('description', '')
            )
            cv.save()
            messages.success(request, 'CV added successfully!')
            return redirect('mongodb_admin:cv_list')
        except Exception as e:
            messages.error(request, f'Error adding CV: {str(e)}')
    
    return render(request, 'admin/cv_form.html', {'title': 'Add CV'})
