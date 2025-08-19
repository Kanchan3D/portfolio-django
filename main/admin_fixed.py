"""
Simple admin interface for MongoDB models
Since we're using MongoDB exclusively, we'll create a basic admin interface
that shows MongoDB data status and provides links to manage content.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.contrib import messages

# Admin site customization
admin.site.site_header = "Kanchan's Portfolio - MongoDB Admin"
admin.site.site_title = "Portfolio MongoDB Admin"
admin.site.index_title = "MongoDB Content Management"

# Custom admin index view to show MongoDB status
def custom_admin_index(request):
    """Custom admin index view with MongoDB status"""
    try:
        from .models import Certificate, CV, Project
        
        # Get counts from MongoDB
        certificates_count = Certificate.objects.count()
        projects_count = Project.objects.count()
        cvs_count = CV.objects.count()
        
        success_message = format_html(
            '<div style="background: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 5px; margin: 20px 0;">'
            '<h3 style="color: #155724; margin-top: 0;">📊 MongoDB Atlas Status</h3>'
            '<p style="color: #155724; margin: 5px 0;"><strong>✅ Connected successfully</strong></p>'
            '<p style="color: #155724; margin: 5px 0;">📄 Certificates: {} documents</p>'
            '<p style="color: #155724; margin: 5px 0;">🚀 Projects: {} documents</p>'
            '<p style="color: #155724; margin: 5px 0;">📝 CVs: {} documents</p>'
            '<hr style="border-color: #c3e6cb;">'
            '<p style="color: #155724; margin: 5px 0;"><strong>💡 Quick Links:</strong></p>'
            '<ul style="color: #155724; margin: 10px 0; padding-left: 20px;">'
            '<li><a href="/" target="_blank">View Portfolio Home</a></li>'
            '<li><a href="/certification/" target="_blank">View Certificates</a></li>'
            '<li><a href="/projects/" target="_blank">View Projects</a></li>'
            '</ul>'
            '<p style="color: #155724; margin: 5px 0;"><strong>💡 Add Content via Django Shell:</strong></p>'
            '<pre style="background: #f8f9fa; padding: 10px; border-radius: 3px; font-size: 12px;">python manage.py shell -c "from main.models import Certificate; ..."</pre>'
            '</div>',
            certificates_count, projects_count, cvs_count
        )
        
        messages.success(request, success_message)
        
    except Exception as e:
        error_message = format_html(
            '<div style="background: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 5px; margin: 20px 0;">'
            '<h3 style="color: #721c24; margin-top: 0;">⚠️ MongoDB Connection Error</h3>'
            '<p style="color: #721c24;">Error: {}</p>'
            '<p style="color: #721c24;">Please check your MongoDB Atlas connection in .env file.</p>'
            '</div>',
            str(e)
        )
        messages.error(request, error_message)
    
    # Call the original admin index view
    from django.contrib.admin.sites import AdminSite
    original_index = AdminSite.index
    return original_index(admin.site, request)

# Replace the admin site index method
admin.site.index = custom_admin_index
