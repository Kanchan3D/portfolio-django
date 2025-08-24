#!/usr/bin/env python3
"""
Script to check MongoDB data for profile photos and project images
"""
import os
import sys
import django

# Add the project path to sys.path
sys.path.append('/Users/kkd/code/Portfolio/v1.1/djangoPortfolio')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

from main.models import Profile, Project

def check_profile_data():
    """Check profile data including photo URL"""
    print("=== PROFILE DATA ===")
    try:
        profile = Profile.objects.first()
        if profile:
            print(f"Name: {profile.name}")
            print(f"Profile Photo URL: {profile.profile_photo_url}")
            print(f"Email: {profile.email}")
            print("✅ Profile found")
        else:
            print("❌ No profile found in database")
    except Exception as e:
        print(f"❌ Error fetching profile: {e}")

def check_project_data():
    """Check project data including image URLs"""
    print("\n=== PROJECT DATA ===")
    try:
        projects = Project.objects.all()
        if projects:
            print(f"Total projects: {len(projects)}")
            for i, project in enumerate(projects, 1):
                print(f"\n{i}. {project.title}")
                print(f"   Image URL: {project.image_url}")
                print(f"   Is Featured: {project.is_featured}")
        else:
            print("❌ No projects found in database")
    except Exception as e:
        print(f"❌ Error fetching projects: {e}")

def main():
    print("Checking MongoDB data for Portfolio application...")
    check_profile_data()
    check_project_data()
    print("\n=== CHECK COMPLETE ===")

if __name__ == "__main__":
    main()
