from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import messages
from .models import DjangoCertificate, DjangoCV, DjangoProject, Certificate, CV, Project

@admin.register(DjangoCertificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['title', 'issuer', 'issue_date', 'is_featured', 'display_order', 'pdf_link']
    list_filter = ['is_featured', 'issuer', 'issue_date']
    search_fields = ['title', 'issuer', 'description']
    list_editable = ['is_featured', 'display_order']
    ordering = ['display_order', '-issue_date']
    
    fieldsets = (
        ('Certificate Information', {
            'fields': ('title', 'issuer', 'description')
        }),
        ('PDF Link', {
            'fields': ('pdf_url',),
            'description': 'Provide the direct URL to the PDF certificate'
        }),
        ('Display Settings', {
            'fields': ('is_featured', 'display_order'),
            'description': 'Control how the certificate appears on the website'
        }),
    )
    
    def pdf_link(self, obj):
        if obj.pdf_url:
            return format_html(
                '<a href="{}" target="_blank" class="button">View PDF</a>',
                obj.pdf_url
            )
        return "No PDF"
    pdf_link.short_description = "PDF"
    
    def save_model(self, request, obj, form, change):
        # Save to Django model
        super().save_model(request, obj, form, change)
        
        # Sync to MongoDB
        try:
            if change:
                # Update existing MongoDB document
                mongo_cert = Certificate.objects(title=obj.title, issuer=obj.issuer).first()
                if mongo_cert:
                    mongo_cert.title = obj.title
                    mongo_cert.issuer = obj.issuer
                    mongo_cert.pdf_url = obj.pdf_url
                    mongo_cert.description = obj.description
                    mongo_cert.is_featured = obj.is_featured
                    mongo_cert.display_order = obj.display_order
                    mongo_cert.save()
                else:
                    # Create new if not found
                    Certificate(
                        title=obj.title,
                        issuer=obj.issuer,
                        pdf_url=obj.pdf_url,
                        description=obj.description,
                        is_featured=obj.is_featured,
                        display_order=obj.display_order
                    ).save()
            else:
                # Create new MongoDB document
                Certificate(
                    title=obj.title,
                    issuer=obj.issuer,
                    pdf_url=obj.pdf_url,
                    description=obj.description,
                    is_featured=obj.is_featured,
                    display_order=obj.display_order
                ).save()
            
            messages.success(request, f'Certificate "{obj.title}" synced to MongoDB successfully!')
        except Exception as e:
            messages.error(request, f'Error syncing to MongoDB: {str(e)}')

@admin.register(DjangoCV)
class CVAdmin(admin.ModelAdmin):
    list_display = ['title', 'version', 'is_active', 'upload_date', 'pdf_link']
    list_filter = ['is_active', 'upload_date']
    search_fields = ['title', 'version', 'description']
    list_editable = ['is_active']
    ordering = ['-upload_date']
    
    fieldsets = (
        ('CV Information', {
            'fields': ('title', 'version', 'description')
        }),
        ('PDF Link', {
            'fields': ('pdf_url',),
            'description': 'Provide the direct URL to your CV/Resume PDF'
        }),
        ('Status', {
            'fields': ('is_active',),
            'description': 'Mark as active to display this CV on the website'
        }),
    )
    
    def pdf_link(self, obj):
        if obj.pdf_url:
            return format_html(
                '<a href="{}" target="_blank" class="button">View PDF</a>',
                obj.pdf_url
            )
        return "No PDF"
    pdf_link.short_description = "PDF"
    
    def save_model(self, request, obj, form, change):
        # Save to Django model
        super().save_model(request, obj, form, change)
        
        # Sync to MongoDB
        try:
            if change:
                # Update existing MongoDB document
                mongo_cv = CV.objects(title=obj.title, version=obj.version).first()
                if mongo_cv:
                    mongo_cv.title = obj.title
                    mongo_cv.pdf_url = obj.pdf_url
                    mongo_cv.version = obj.version
                    mongo_cv.is_active = obj.is_active
                    mongo_cv.description = obj.description
                    mongo_cv.save()
                else:
                    # Create new if not found
                    CV(
                        title=obj.title,
                        pdf_url=obj.pdf_url,
                        version=obj.version,
                        is_active=obj.is_active,
                        description=obj.description
                    ).save()
            else:
                # Create new MongoDB document
                CV(
                    title=obj.title,
                    pdf_url=obj.pdf_url,
                    version=obj.version,
                    is_active=obj.is_active,
                    description=obj.description
                ).save()
            
            messages.success(request, f'CV "{obj.title}" synced to MongoDB successfully!')
        except Exception as e:
            messages.error(request, f'Error syncing to MongoDB: {str(e)}')

# Custom admin actions
def sync_certificates_to_mongo(modeladmin, request, queryset):
    """Sync selected certificates to MongoDB"""
    count = 0
    for cert in queryset:
        try:
            mongo_cert, created = Certificate.objects.get_or_create(
                title=cert.title,
                issuer=cert.issuer,
                defaults={
                    'pdf_url': cert.pdf_url,
                    'description': cert.description,
                    'is_featured': cert.is_featured,
                    'display_order': cert.display_order
                }
            )
            if not created:
                mongo_cert.pdf_url = cert.pdf_url
                mongo_cert.description = cert.description
                mongo_cert.is_featured = cert.is_featured
                mongo_cert.display_order = cert.display_order
                mongo_cert.save()
            count += 1
        except Exception as e:
            messages.error(request, f'Error syncing {cert.title}: {str(e)}')
    
    messages.success(request, f'Successfully synced {count} certificates to MongoDB')

sync_certificates_to_mongo.short_description = "Sync selected certificates to MongoDB"

# Add the action to CertificateAdmin
CertificateAdmin.actions = [sync_certificates_to_mongo]

@admin.register(DjangoProject)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'description_short', 'technologies_short', 'is_featured', 'github_link', 'live_link']
    list_filter = ['is_featured', 'created_date']
    search_fields = ['title', 'description', 'technologies']
    list_editable = ['is_featured']
    ordering = ['-created_date']
    
    fieldsets = (
        ('Project Information', {
            'fields': ('title', 'description')
        }),
        ('Visual & Technical Details', {
            'fields': ('image_url', 'technologies'),
            'description': 'Image URL and comma-separated technologies'
        }),
        ('Links', {
            'fields': ('github_url', 'live_url'),
            'description': 'GitHub repository and live demo links'
        }),
        ('Display Settings', {
            'fields': ('is_featured',),
            'description': 'Control whether this project appears on the portfolio'
        }),
    )
    
    def description_short(self, obj):
        return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
    description_short.short_description = "Description"
    
    def technologies_short(self, obj):
        techs = obj.get_technologies_list()
        return ", ".join(techs[:3]) + ("..." if len(techs) > 3 else "")
    technologies_short.short_description = "Technologies"
    
    def github_link(self, obj):
        if obj.github_url:
            return format_html(
                '<a href="{}" target="_blank" class="button">GitHub</a>',
                obj.github_url
            )
        return "No GitHub"
    github_link.short_description = "GitHub"
    
    def live_link(self, obj):
        if obj.live_url:
            return format_html(
                '<a href="{}" target="_blank" class="button">Live Demo</a>',
                obj.live_url
            )
        return "No Demo"
    live_link.short_description = "Live Demo"

# Admin site customization
admin.site.site_header = "Kanchan's Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to Portfolio Administration"
