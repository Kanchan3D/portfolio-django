from django.shortcuts import render
from django.http import Http404, JsonResponse
from .models import Certificate, CV, Project, Profile

def get_profile_data():
    """Get profile data with fallback defaults"""
    try:
        # Get the single profile (there should only be one)
        profile = Profile.objects.first()
        
        if not profile:
            print(f"⚠️ No profile found in database, using default values")
        else:
            print(f"✅ Using profile: {profile.name} (Active: {profile.is_active})")
            
    except Exception as e:
        print(f"⚠️ MongoDB error getting profile: {e}")
        profile = None
    
    return {
        'name': profile.name if profile and profile.name else 'Kanchan Dasila',
        'title': profile.title if profile and profile.title else 'Full Stack Web Developer',
        'bio': profile.bio if profile and profile.bio else None,
        'email': profile.email if profile and profile.email else 'Kanchan.Dasila1@gmail.com',
        'phone': profile.phone if profile and profile.phone else None,
        'location': profile.location if profile and profile.location else 'Jalandhar',
        'linkedin_url': profile.linkedin_url if profile and profile.linkedin_url else 'https://www.linkedin.com/in/kanchan3',
        'github_url': profile.github_url if profile and profile.github_url else 'https://github.com/Kanchan3D',
        'twitter_url': profile.twitter_url if profile and profile.twitter_url else None,
        'instagram_url': getattr(profile, 'instagram_url', None) if profile else None,
        'website_url': profile.website_url if profile and profile.website_url else None,
        'profile_photo_url': profile.profile_photo_url if profile and profile.profile_photo_url else None,
        'resume_url': profile.resume_url if profile and profile.resume_url else None,
        'years_experience': profile.years_experience if profile and profile.years_experience else 0,
        'skills': profile.skills if profile and profile.skills else None,
        'languages': profile.languages if profile and profile.languages else None,
        'is_available_for_work': profile.is_available_for_work if profile else True,
    }

def home(request):
    # Get profile data with fallbacks
    profile_data = get_profile_data()
    
    # Get CV URL
    try:
        active_cv = CV.objects(is_current=True).first()
        cv_url = active_cv.pdf_url if active_cv else (profile_data['resume_url'] if profile_data['resume_url'] else "https://drive.google.com/file/d/1yzdrXJG6MOCjmjz1-GzCCpPxSefCiVT3/view")
    except Exception as e:
        print(f"⚠️ MongoDB error getting CV: {e}")
        cv_url = "https://drive.google.com/file/d/1yzdrXJG6MOCjmjz1-GzCCpPxSefCiVT3/view"
    
    context = {
        'title': f'Home - {profile_data["name"]} Portfolio',
        'page': 'home',
        'cv_url': cv_url,
        'profile': profile_data
    }
    return render(request, 'main/home.html', context)

def about(request):
    # Get profile data with fallbacks
    profile_data = get_profile_data()
    
    skill_icons = [
        {"src": "https://skillicons.dev/icons?i=c", "alt": "C"},
        {"src": "https://skillicons.dev/icons?i=cpp", "alt": "C++"},
        {"src": "https://skillicons.dev/icons?i=java", "alt": "Java"},
        {"src": "https://skillicons.dev/icons?i=python", "alt": "Python"},
        {"src": "https://skillicons.dev/icons?i=javascript", "alt": "JavaScript"},
        {"src": "https://skillicons.dev/icons?i=typescript", "alt": "TypeScript"},
        {"src": "https://skillicons.dev/icons?i=html", "alt": "HTML"},
        {"src": "https://skillicons.dev/icons?i=css", "alt": "CSS"},
        {"src": "https://skillicons.dev/icons?i=tailwind", "alt": "Tailwind CSS"},
        {"src": "https://skillicons.dev/icons?i=react", "alt": "React"},
        {"src": "https://skillicons.dev/icons?i=next", "alt": "Next.js"},
        {"src": "https://skillicons.dev/icons?i=vite", "alt": "Vite"},
        {"src": "https://skillicons.dev/icons?i=nodejs", "alt": "Node.js"},
        {"src": "https://skillicons.dev/icons?i=express", "alt": "Express.js"},
        {"src": "https://skillicons.dev/icons?i=mongodb", "alt": "MongoDB"},
        {"src": "https://skillicons.dev/icons?i=mysql", "alt": "MySQL"},
        {"src": "https://skillicons.dev/icons?i=postgres", "alt": "PostgreSQL"},
        {"src": "https://skillicons.dev/icons?i=prisma", "alt": "Prisma"},
        {"src": "https://skillicons.dev/icons?i=aws", "alt": "AWS"},
        {"src": "https://skillicons.dev/icons?i=gcp", "alt": "Google Cloud"},
        {"src": "https://skillicons.dev/icons?i=firebase", "alt": "Firebase"},
        {"src": "https://skillicons.dev/icons?i=docker", "alt": "Docker"},
        {"src": "https://skillicons.dev/icons?i=vercel", "alt": "Vercel"},
        {"src": "https://skillicons.dev/icons?i=replit", "alt": "Replit"},
        {"src": "https://skillicons.dev/icons?i=git", "alt": "Git"},
        {"src": "https://skillicons.dev/icons?i=github", "alt": "GitHub"},
        {"src": "https://skillicons.dev/icons?i=gitlab", "alt": "GitLab"},
        {"src": "https://skillicons.dev/icons?i=vscode", "alt": "VS Code"},
        {"src": "https://skillicons.dev/icons?i=powershell", "alt": "PowerShell"},
        {"src": "https://skillicons.dev/icons?i=postman", "alt": "Postman"},
        {"src": "https://skillicons.dev/icons?i=linkedin", "alt": "LinkedIn"},
        {"src": "https://skillicons.dev/icons?i=discord", "alt": "Discord"},
        {"src": "https://skillicons.dev/icons?i=kali", "alt": "Kali Linux"},
        {"src": "https://skillicons.dev/icons?i=linux", "alt": "Linux"},
        {"src": "https://skillicons.dev/icons?i=jquery", "alt": "jQuery"},
    ]
    
    context = {
        'title': f'About - {profile_data["name"]} Portfolio',
        'page': 'about',
        'skill_icons': skill_icons,
        'profile': profile_data
    }
    return render(request, 'main/about.html', context)

def projects(request):
    # Get projects from MongoDB only
    try:
        mongo_projects = Project.objects(is_featured=True)
        projects_list = []
        
        for project in mongo_projects:
            projects_list.append({
                'title': project.title,
                'description': project.description,
                'image': project.image_url or 'assets/project/default.jpg',
                'technologies': project.get_technologies_list(),
                'github': project.github_url or '#',
                'live': project.live_url or '#'
            })
            
        # If no featured projects, show all projects
        if not projects_list:
            all_projects = Project.objects.all()
            for project in all_projects:
                projects_list.append({
                    'title': project.title,
                    'description': project.description,
                    'image': project.image_url or 'assets/project/default.jpg',
                    'technologies': project.get_technologies_list(),
                    'github': project.github_url or '#',
                    'live': project.live_url or '#'
                })
                
    except Exception as e:
        print(f"⚠️ MongoDB error getting projects: {e}")
        # Fallback to default projects if MongoDB fails
        projects_list = [
            {
                'title': 'E-Commerce Platform',
                'description': 'Full-stack e-commerce application with React, Node.js, and MongoDB',
                'image': 'assets/project/ecom.jpg',
                'technologies': ['React', 'Node.js', 'MongoDB', 'Express'],
                'github': '#',
                'live': '#'
            },
            {
                'title': 'Blogging Platform',
                'description': 'A modern blogging platform with user authentication and content management',
                'image': 'assets/project/blogging.jpg',
                'technologies': ['React', 'Django', 'PostgreSQL'],
                'github': '#',
                'live': '#'
            },
            {
                'title': 'URL Shortener',
                'description': 'URL shortening service with analytics and custom domains',
                'image': 'assets/project/url-shortener.jpg',
                'technologies': ['Node.js', 'Express', 'MongoDB'],
                'github': '#',
                'live': '#'
            },
            {
                'title': 'LeetMetric',
                'description': 'LeetCode problem tracking and analytics dashboard',
                'image': 'assets/project/leetmetric.png',
                'technologies': ['React', 'API Integration', 'Charts.js'],
                'github': '#',
                'live': '#'
            },
            {
                'title': 'Learning Management System',
                'description': 'Complete LMS with course management and student tracking',
                'image': 'assets/project/lms.png',
                'technologies': ['React', 'Node.js', 'MySQL'],
                'github': '#',
                'live': '#'
            },
            {
                'title': 'Voting System',
                'description': 'Secure digital voting system with blockchain technology',
                'image': 'assets/project/Voting.jpg',
                'technologies': ['React', 'Blockchain', 'Web3'],
                'github': '#',
                'live': '#'
            }
        ]
    
    # Get profile data with fallbacks
    profile_data = get_profile_data()
    
    context = {
        'title': f'Projects - {profile_data["name"]} Portfolio',
        'page': 'projects',
        'projects': projects_list,
        'profile': profile_data
    }
    return render(request, 'main/projects.html', context)

def contact(request):
    # Get profile data with fallbacks
    profile_data = get_profile_data()
    
    context = {
        'title': f'Contact - {profile_data["name"]} Portfolio',
        'page': 'contact',
        'profile': profile_data
    }
    return render(request, 'main/contact.html', context)

def mywork(request):
    # Get profile data with fallbacks
    profile_data = get_profile_data()
    
    context = {
        'title': f'My Work - {profile_data["name"]} Portfolio',
        'page': 'mywork',
        'profile': profile_data
    }
    return render(request, 'main/mywork.html', context)

def certification(request):
    # Get certificates from MongoDB only
    try:
        mongo_certificates = Certificate.objects(is_featured=True)
        certifications_list = []
        
        for cert in mongo_certificates:
            certifications_list.append({
                'title': cert.title,
                'issuer': cert.issuer,
                'file': cert.pdf_url,
                'description': cert.description,
                'issue_date': cert.issue_date
            })
            
        # If no featured certificates, show all certificates
        if not certifications_list:
            all_certificates = Certificate.objects.all()
            for cert in all_certificates:
                certifications_list.append({
                    'title': cert.title,
                    'issuer': cert.issuer,
                    'file': cert.pdf_url,
                    'description': cert.description,
                    'issue_date': cert.issue_date
                })
                
    except Exception as e:
        print(f"⚠️ MongoDB error getting certificates: {e}")
        # Fallback to default certificates if MongoDB fails
        certifications_list = [
            {
                'title': 'Advanced JavaScript',
                'issuer': 'Coursera',
                'file': 'assets/Certificates/Advanced JavaScript.pdf',
                'description': 'Advanced concepts in JavaScript programming'
            },
            {
                'title': 'Advanced React',
                'issuer': 'Coursera',
                'file': 'assets/Certificates/Advanced React.pdf',
                'description': 'Advanced React development techniques'
            },
            {
                'title': 'Command Line Basics',
                'issuer': 'Coursera',
                'file': 'assets/Certificates/Command Line Basics.pdf',
                'description': 'Fundamentals of command line interface'
            },
            {
                'title': 'Frontend Development',
                'issuer': 'Coursera',
                'file': 'assets/Certificates/KanchanFrontend.pdf',
                'description': 'Complete frontend development course'
            },
            {
                'title': 'Learn Express.js',
                'issuer': 'Online Course',
                'file': 'assets/Certificates/Learn Express.js.pdf',
                'description': 'Express.js framework for Node.js'
            },
            {
                'title': 'Learn Next.js',
                'issuer': 'Online Course',
                'file': 'assets/Certificates/Learn Next.js.pdf',
                'description': 'Next.js React framework'
            },
            {
                'title': 'Learn Node.js',
                'issuer': 'Online Course',
                'file': 'assets/Certificates/Learn Node.js.pdf',
                'description': 'Node.js backend development'
            },
            {
                'title': 'Learn TypeScript',
                'issuer': 'Online Course',
                'file': 'assets/Certificates/Learn TypeScript.pdf',
                'description': 'TypeScript programming language'
            },
            {
                'title': 'Node.js MOOC',
                'issuer': 'Online Course',
                'file': 'assets/Certificates/NodejsMOOC.pdf',
                'description': 'Comprehensive Node.js course'
            },
            {
                'title': 'Ethical Hacking',
                'issuer': 'Cybersecurity Course',
                'file': 'assets/Certificates/EthicalHacking.pdf',
                'description': 'Ethical hacking and cybersecurity'
            }
        ]
    
    # Get profile data with fallbacks
    profile_data = get_profile_data()
    
    context = {
        'title': f'Certifications - {profile_data["name"]} Portfolio',
        'page': 'certification',
        'certifications': certifications_list,
        'profile': profile_data
    }
    return render(request, 'main/certification.html', context)

def profile_api(request):
    """API endpoint to get profile data for frontend"""
    try:
        profile_data = get_profile_data()
        
        # Format skills and languages as arrays
        formatted_profile = profile_data.copy()
        formatted_profile['skills'] = profile_data['skills'].split(',') if profile_data['skills'] else []
        formatted_profile['languages'] = profile_data['languages'].split(',') if profile_data['languages'] else []
        
        return JsonResponse({
            'success': True,
            'message': 'Profile retrieved successfully',
            'data': formatted_profile
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error retrieving profile: {str(e)}',
            'data': None
        }, status=500)
