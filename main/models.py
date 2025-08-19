from django.db import models
from mongoengine import Document, StringField, URLField, DateTimeField, BooleanField, IntField, EmailField
from datetime import datetime

# MongoDB Models using MongoEngine

class Profile(Document):
    """Personal profile information for the portfolio"""
    # Basic Information
    name = StringField(max_length=100, required=True, help_text="Full name")
    title = StringField(max_length=200, help_text="Professional title (e.g., 'Full Stack Developer')")
    bio = StringField(max_length=1000, help_text="Short biography or description")
    
    # Contact Information
    email = EmailField(required=True, help_text="Primary email address")
    phone = StringField(max_length=20, help_text="Phone number")
    location = StringField(max_length=100, help_text="Current location (e.g., 'New York, USA')")
    
    # Social Media & Professional Links
    linkedin_url = URLField(help_text="LinkedIn profile URL")
    github_url = URLField(help_text="GitHub profile URL")
    twitter_url = URLField(help_text="Twitter profile URL")
    instagram_url = URLField(help_text="Instagram profile URL")
    website_url = URLField(help_text="Personal website URL")
    
    # Media
    profile_photo_url = URLField(help_text="Profile photo/avatar URL")
    resume_url = URLField(help_text="Current resume/CV URL")
    
    # Professional Details
    years_experience = IntField(min_value=0, help_text="Years of professional experience")
    skills = StringField(max_length=500, help_text="Comma-separated list of key skills")
    languages = StringField(max_length=200, help_text="Programming languages you know")
    
    # Settings
    is_active = BooleanField(default=True, help_text="Active profile (only one should be active)")
    is_available_for_work = BooleanField(default=True, help_text="Available for new opportunities")
    
    # Timestamps
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'profile',
        'ordering': ['-is_active', '-updated_at']
    }
    
    def __str__(self):
        return f"{self.name} - {self.title}"
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        # Ensure only one active profile
        if self.is_active:
            Profile.objects(is_active=True).update(is_active=False)
        return super().save(*args, **kwargs)

class Certificate(Document):
    title = StringField(max_length=200, required=True)
    issuer = StringField(max_length=200, required=True)
    pdf_url = URLField(required=True, help_text="Direct link to the PDF certificate")
    issue_date = DateTimeField(default=datetime.now)
    description = StringField(max_length=500, help_text="Brief description of the certificate")
    is_featured = BooleanField(default=True, help_text="Show on certification page")
    display_order = IntField(default=0, help_text="Order to display (lower numbers first)")
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'certificates',
        'ordering': ['display_order', '-issue_date']
    }
    
    def __str__(self):
        return f"{self.title} - {self.issuer}"
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

class CV(Document):
    title = StringField(max_length=100, required=True, default="My Resume")
    pdf_url = URLField(required=True, help_text="Direct link to the CV/Resume PDF")
    version = StringField(max_length=50, default="1.0")
    is_active = BooleanField(default=True, help_text="Currently active CV")
    description = StringField(max_length=300, help_text="Brief description or version notes")
    upload_date = DateTimeField(default=datetime.now)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'cv_resumes',
        'ordering': ['-upload_date']
    }
    
    def __str__(self):
        return f"{self.title} (v{self.version})"
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        # Ensure only one CV is active at a time
        if self.is_active:
            CV.objects(is_active=True).update(is_active=False)
        return super().save(*args, **kwargs)
    
    @classmethod
    def get_active_cv(cls):
        """Get the currently active CV"""
        try:
            return cls.objects(is_active=True).first()
        except:
            return None

class Project(Document):
    title = StringField(max_length=200, required=True)
    description = StringField(max_length=1000, required=True)
    image_url = URLField(help_text="Project screenshot or image URL")
    github_url = URLField(help_text="GitHub repository URL")
    live_url = URLField(help_text="Live demo URL")
    technologies = StringField(max_length=500, help_text="Comma-separated list of technologies")
    is_featured = BooleanField(default=True)
    display_order = IntField(default=0)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'projects',
        'ordering': ['display_order', '-created_at']
    }
    
    def __str__(self):
        return self.title
    
    def get_technologies_list(self):
        """Return technologies as a list"""
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(',')]
        return []
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

# Django Models (for admin interface compatibility)
class DjangoCertificate(models.Model):
    """Django model for admin interface - syncs with MongoDB"""
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    pdf_url = models.URLField(help_text="Direct link to the PDF certificate")
    issue_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=500, blank=True, help_text="Brief description")
    is_featured = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Certificate"
        verbose_name_plural = "Certificates"
        ordering = ['display_order', '-issue_date']
    
    def __str__(self):
        return f"{self.title} - {self.issuer}"

class DjangoCV(models.Model):
    """Django model for admin interface - syncs with MongoDB"""
    title = models.CharField(max_length=100, default="My Resume")
    pdf_url = models.URLField(help_text="Direct link to the CV/Resume PDF")
    version = models.CharField(max_length=50, default="1.0")
    is_active = models.BooleanField(default=True, help_text="Currently active CV")
    description = models.TextField(max_length=300, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "CV/Resume"
        verbose_name_plural = "CV/Resumes"
        ordering = ['-upload_date']
    
    def __str__(self):
        return f"{self.title} (v{self.version})"

class DjangoProject(models.Model):
    """Django model for admin interface - syncs with MongoDB"""
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    image_url = models.URLField(blank=True, help_text="Direct link to project image")
    technologies = models.CharField(max_length=500, help_text="Comma-separated list of technologies")
    github_url = models.URLField(blank=True, help_text="GitHub repository link")
    live_url = models.URLField(blank=True, help_text="Live demo link")
    is_featured = models.BooleanField(default=True, help_text="Show on portfolio")
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['-created_date']
    
    def get_technologies_list(self):
        """Return technologies as a list"""
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]
    
    def __str__(self):
        return self.title
