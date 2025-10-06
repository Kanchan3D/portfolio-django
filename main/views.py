from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
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

def get_resume_url():
    profile = Profile.objects.first()
    if profile and profile.resume_url:
        return profile.resume_url
    return "https://drive.google.com/file/d/1yzdrXJG6MOCjmjz1-GzCCpPxSefCiVT3/view"

def home(request):
    # Get profile data with fallbacks
    profile_data = get_profile_data()
    cv_url = get_resume_url()
    
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
    # Get profile data with fallbacks
    profile_data = get_profile_data()
    cv_url = get_resume_url()
    
    # Get projects from MongoDB only
    try:
        mongo_projects = Project.objects(is_featured=True)
        projects_list = []
        
        for project in mongo_projects:
            projects_list.append({
                'title': project.title,
                'description': project.description,
                'image': project.image_url or '',
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
                    'image': project.image_url or '',
                    'technologies': project.get_technologies_list(),
                    'github': project.github_url or '#',
                    'live': project.live_url or '#'
                })
                
    except Exception as e:
        print(f"⚠️ MongoDB error getting projects: {e}")
        projects_list = []
    
    context = {
        'title': f'Projects - {profile_data["name"]} Portfolio',
        'page': 'projects',
        'cv_url': cv_url,
        'profile': profile_data,
        'projects': projects_list
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
        # Fallback to default certificates based on actual certificate files
        certifications_list = [
            {
                'title': 'Advanced JavaScript',
                'issuer': 'Programming Course Platform',
                'file': 'assets/Certificates/Advanced JavaScript.pdf',
                'description': 'Advanced JavaScript concepts including ES6+, async programming, DOM manipulation, and modern JavaScript features for building dynamic web applications.'
            },
            {
                'title': 'Advanced React',
                'issuer': 'React Development Platform',
                'file': 'assets/Certificates/Advanced React.pdf',
                'description': 'Advanced React concepts including hooks, context API, performance optimization, and modern React patterns for building scalable applications.'
            },
            {
                'title': 'Command Line Basics',
                'issuer': 'System Administration Course',
                'file': 'assets/Certificates/Command Line Basics.pdf',
                'description': 'Fundamentals of command line interface, terminal navigation, file operations, and essential CLI tools for developers.'
            },
            {
                'title': 'Full Stack Development',
                'issuer': 'Coursera',
                'file': 'assets/Certificates/Coursera BDFV853TMJPF.pdf',
                'description': 'Comprehensive full stack web development certification covering frontend, backend, and database technologies.'
            },
            {
                'title': 'C++ Programming',
                'issuer': 'Programming Institute',
                'file': 'assets/Certificates/cpp1.pdf',
                'description': 'Object-oriented programming with C++, data structures, algorithms, and memory management fundamentals.'
            },
            {
                'title': 'Ethical Hacking',
                'issuer': 'Cybersecurity Institute',
                'file': 'assets/Certificates/EthicalHacking.pdf',
                'description': 'Ethical hacking methodologies, penetration testing, vulnerability assessment, and cybersecurity best practices.'
            },
            {
                'title': 'Google AI Essentials',
                'issuer': 'Google',
                'file': 'assets/Certificates/Gai1.pdf',
                'description': 'Artificial Intelligence fundamentals, machine learning basics, and AI applications in modern technology.'
            },
            {
                'title': 'Frontend Development Certification',
                'issuer': 'Web Development Academy',
                'file': 'assets/Certificates/KanchanFrontend.pdf',
                'description': 'Complete frontend development certification covering HTML5, CSS3, JavaScript, responsive design, and modern frameworks.'
            },
            {
                'title': 'Learn Express.js',
                'issuer': 'Backend Development Platform',
                'file': 'assets/Certificates/Learn Express.js.pdf',
                'description': 'Express.js framework for Node.js including middleware, routing, RESTful APIs, and server-side development.'
            },
            {
                'title': 'Learn Next.js',
                'issuer': 'React Framework Course',
                'file': 'assets/Certificates/Learn Next.js.pdf',
                'description': 'Next.js React framework covering server-side rendering, static generation, API routes, and modern web development.'
            },
            {
                'title': 'Learn Node.js',
                'issuer': 'Backend Development Platform',
                'file': 'assets/Certificates/Learn Node.js.pdf',
                'description': 'Node.js runtime environment for backend development, including asynchronous programming and server-side JavaScript.'
            },
            {
                'title': 'Learn TypeScript',
                'issuer': 'Programming Language Course',
                'file': 'assets/Certificates/Learn TypeScript.pdf',
                'description': 'TypeScript programming language covering static typing, interfaces, generics, and modern JavaScript development.'
            },
            {
                'title': 'Node.js MOOC',
                'issuer': 'Online Learning Platform',
                'file': 'assets/Certificates/NodejsMOOC.pdf',
                'description': 'Massive Open Online Course on Node.js covering comprehensive backend development with JavaScript runtime.'
            },
            {
                'title': 'Portfolio Project',
                'issuer': 'Project Development Course',
                'file': 'assets/Certificates/pf1.pdf',
                'description': 'Portfolio development project showcasing web development skills and modern design principles.'
            },
            {
                'title': 'PHP Development',
                'issuer': 'Web Development Platform',
                'file': 'assets/Certificates/phpmooc.pdf',
                'description': 'PHP programming language for web development including server-side scripting and dynamic web applications.'
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

@csrf_exempt
@require_http_methods(["POST"])
def contact_submit(request):
    """Handle contact form submission"""
    try:
        # Parse JSON data
        data = json.loads(request.body)
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()
        
        # Validate required fields
        if not all([name, email, subject, message]):
            return JsonResponse({
                'success': False,
                'message': 'All fields are required.'
            }, status=400)
        
        # Get profile data for recipient email
        profile_data = get_profile_data()
        recipient_email = profile_data.get('email', 'kanchandasila31@gmail.com')
        
        # Prepare email content
        email_subject = f"Portfolio Contact: {subject}"
        email_body = f"""
New message from your portfolio website:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This message was sent from your portfolio contact form.
        """
        
        # Send email (if email settings are configured)
        try:
            if hasattr(settings, 'EMAIL_HOST') and settings.EMAIL_HOST:
                send_mail(
                    email_subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient_email],
                    fail_silently=False,
                )
                print(f"✅ Email sent to {recipient_email}")
            else:
                print(f"⚠️ Email settings not configured. Message would be sent to: {recipient_email}")
                print(f"Subject: {email_subject}")
                print(f"From: {name} ({email})")
                print(f"Message: {message}")
        except Exception as email_error:
            print(f"⚠️ Email sending failed: {email_error}")
            # Don't fail the request if email fails - still return success
        
        return JsonResponse({
            'success': True,
            'message': 'Thank you! Your message has been sent successfully. 😇'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data.'
        }, status=400)
    except Exception as e:
        print(f"❌ Contact form error: {e}")
        return JsonResponse({
            'success': False,
            'message': 'Failed to send message, please try again. 🥲'
        }, status=500)


def custom_404_view(request, exception=None):
    """Custom 404 error handler"""
    profile = get_profile_data()
    return render(request, 'main/404.html', {
        'profile': profile,
        'page': '404',
        'title': '404 - Page Not Found'
    }, status=404)
