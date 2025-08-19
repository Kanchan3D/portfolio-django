"""
Simple admin interface for MongoDB models
Since we're using MongoDB exclusively, we'll create a basic admin interface
that shows MongoDB data status and provides links to manage content.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import messages

# Create a simple admin interface for MongoDB status
class MongoDBAdminSite(admin.AdminSite):
    site_header = "Kanchan's Portfolio - MongoDB Admin"
    site_title = "Portfolio MongoDB Admin"
    index_title = "MongoDB Content Management"
    
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        try:
            from .models import Certificate, CV, Project
            
            # Get counts from MongoDB
            certificates_count = Certificate.objects.count()
            projects_count = Project.objects.count()
            cvs_count = CV.objects.count()
            
            extra_context.update({
                'mongodb_status': 'Connected',
                'certificates_count': certificates_count,
                'projects_count': projects_count,
                'cvs_count': cvs_count,
                'mongodb_info': format_html(
                    '<div style="background: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 5px; margin: 20px 0;">'
                    '<h3 style="color: #155724; margin-top: 0;">📊 MongoDB Atlas Status</h3>'
                    '<p style="color: #155724; margin: 5px 0;"><strong>✅ Connected to MongoDB Atlas</strong></p>'
                    '<p style="color: #155724; margin: 5px 0;">📄 Certificates: {} documents</p>'
                    '<p style="color: #155724; margin: 5px 0;">🚀 Projects: {} documents</p>'
                    '<p style="color: #155724; margin: 5px 0;">📝 CVs: {} documents</p>'
                    '<hr style="border-color: #c3e6cb;">'
                    '<p style="color: #155724; margin: 5px 0;"><strong>💡 Management Tips:</strong></p>'
                    '<ul style="color: #155724; margin: 10px 0; padding-left: 20px;">'
                    '<li>Use the Django shell to add/edit content: <code>python manage.py shell</code></li>'
                    '<li>Populate with sample data: <code>python manage.py populate_mongodb</code></li>'
                    '<li>View your portfolio: <a href="http://127.0.0.1:8001/" target="_blank">http://127.0.0.1:8001/</a></li>'
                    '</ul>'
                    '</div>',
                    certificates_count, projects_count, cvs_count
                )
            })
            
        except Exception as e:
            extra_context.update({
                'mongodb_status': 'Error',
                'mongodb_info': format_html(
                    '<div style="background: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 5px; margin: 20px 0;">'
                    '<h3 style="color: #721c24; margin-top: 0;">⚠️ MongoDB Connection Error</h3>'
                    '<p style="color: #721c24; margin: 5px 0;"><strong>Error:</strong> {}</p>'
                    '<p style="color: #721c24; margin: 5px 0;">Please check your MongoDB Atlas connection settings in .env file.</p>'
                    '</div>',
                    str(e)
                )
            })
        
        return super().index(request, extra_context)

# Admin site customization
admin.site.site_header = "Kanchan's Portfolio - MongoDB Admin"
admin.site.site_title = "Portfolio MongoDB Admin"
admin.site.index_title = "MongoDB Content Management"

# Add the MongoDB status to the admin index
def mongodb_status_view(request):
    """Custom view to show MongoDB status"""
    try:
        from .models import Certificate, CV, Project
        
        certificates_count = Certificate.objects.count()
        projects_count = Project.objects.count()
        cvs_count = CV.objects.count()
        
        status_html = format_html(
            '<div style="background: #d4edda; border: 1px solid #c3e6cb; padding: 15px; border-radius: 5px; margin: 20px 0;">'
            '<h3 style="color: #155724; margin-top: 0;">📊 MongoDB Atlas Status</h3>'
            '<p style="color: #155724; margin: 5px 0;"><strong>✅ Connected successfully</strong></p>'
            '<p style="color: #155724; margin: 5px 0;">📄 Certificates: {} documents</p>'
            '<p style="color: #155724; margin: 5px 0;">🚀 Projects: {} documents</p>'
            '<p style="color: #155724; margin: 5px 0;">📝 CVs: {} documents</p>'
            '</div>',
            certificates_count, projects_count, cvs_count
        )
        
        messages.success(request, status_html)
        
    except Exception as e:
        error_html = format_html(
            '<div style="background: #f8d7da; border: 1px solid #f5c6cb; padding: 15px; border-radius: 5px;">'
            '<h3 style="color: #721c24; margin-top: 0;">⚠️ MongoDB Error</h3>'
            '<p style="color: #721c24;">Error: {}</p>'
            '</div>',
            str(e)
        )
        messages.error(request, error_html)
    
    return admin.site.index(request)

# Override the admin index view
admin.site.index = mongodb_status_view
