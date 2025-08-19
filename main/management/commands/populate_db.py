from django.core.management.base import BaseCommand
from main.models import DjangoCertificate, DjangoCV, Certificate, CV, Project
from datetime import datetime

class Command(BaseCommand):
    help = 'Populate database with sample certificates, CV and projects'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write("Clearing existing data...")
            DjangoCertificate.objects.all().delete()
            DjangoCV.objects.all().delete()
            # Clear MongoDB data if connected
            try:
                Certificate.objects.all().delete()
                CV.objects.all().delete()
                Project.objects.all().delete()
                self.stdout.write(
                    self.style.SUCCESS('✅ Cleared MongoDB data')
                )
            except:
                self.stdout.write(
                    self.style.WARNING('⚠️  MongoDB not connected, skipping MongoDB cleanup')
                )

        # Sample certificates data
        certificates_data = [
            {
                'title': 'Advanced JavaScript',
                'issuer': 'Coursera',
                'pdf_url': 'https://example.com/certificates/advanced-javascript.pdf',
                'description': 'Advanced concepts in JavaScript programming including ES6+, async/await, and modern frameworks',
                'display_order': 1
            },
            {
                'title': 'Advanced React',
                'issuer': 'Coursera',
                'pdf_url': 'https://example.com/certificates/advanced-react.pdf',
                'description': 'Advanced React development techniques including hooks, context, and performance optimization',
                'display_order': 2
            },
            {
                'title': 'Node.js Development',
                'issuer': 'Online Course',
                'pdf_url': 'https://example.com/certificates/nodejs.pdf',
                'description': 'Complete Node.js backend development with Express.js and MongoDB',
                'display_order': 3
            },
            {
                'title': 'Frontend Development',
                'issuer': 'Coursera',
                'pdf_url': 'https://example.com/certificates/frontend.pdf',
                'description': 'Complete frontend development course covering HTML, CSS, JavaScript, and React',
                'display_order': 4
            },
            {
                'title': 'Python Programming',
                'issuer': 'Online Course',
                'pdf_url': 'https://example.com/certificates/python.pdf',
                'description': 'Comprehensive Python programming course with web development focus',
                'display_order': 5
            },
            {
                'title': 'Ethical Hacking',
                'issuer': 'Cybersecurity Institute',
                'pdf_url': 'https://example.com/certificates/ethical-hacking.pdf',
                'description': 'Ethical hacking and penetration testing certification',
                'display_order': 6
            }
        ]

        # Sample CV data
        cv_data = {
            'title': 'Kanchan Dasila - Resume',
            'pdf_url': 'https://drive.google.com/file/d/1yzdrXJG6MOCjmjz1-GzCCpPxSefCiVT3/view',
            'version': '2.0',
            'is_active': True,
            'description': 'Latest resume with updated projects and skills'
        }

        # Sample projects data
        projects_data = [
            {
                'title': 'E-Commerce Platform',
                'description': 'Full-stack e-commerce application with React, Node.js, and MongoDB featuring user authentication, payment integration, and admin dashboard',
                'image_url': 'https://example.com/projects/ecommerce.jpg',
                'github_url': 'https://github.com/Kanchan3D/ecommerce-platform',
                'live_url': 'https://ecommerce-demo.vercel.app',
                'technologies': 'React, Node.js, MongoDB, Express, Stripe API',
                'display_order': 1
            },
            {
                'title': 'LeetMetric Dashboard',
                'description': 'Analytics dashboard for tracking LeetCode progress with interactive charts and performance metrics',
                'image_url': 'https://example.com/projects/leetmetric.jpg',
                'github_url': 'https://github.com/Kanchan3D/leetmetric',
                'live_url': 'https://leetmetric.vercel.app',
                'technologies': 'React, Chart.js, LeetCode API, TypeScript',
                'display_order': 2
            },
            {
                'title': 'Portfolio Website',
                'description': 'Personal portfolio website built with Django and modern web technologies',
                'image_url': 'https://example.com/projects/portfolio.jpg',
                'github_url': 'https://github.com/Kanchan3D/django-portfolio',
                'live_url': 'https://kanchan-portfolio.herokuapp.com',
                'technologies': 'Django, MongoDB, HTML, CSS, JavaScript, Tailwind CSS',
                'display_order': 3
            }
        ]

        # Create certificates
        self.stdout.write("Creating certificates...")
        for cert_data in certificates_data:
            # Create Django model
            django_cert, created = DjangoCertificate.objects.get_or_create(
                title=cert_data['title'],
                issuer=cert_data['issuer'],
                defaults=cert_data
            )
            
            # Create MongoDB document if connected
            try:
                mongo_cert, created = Certificate.objects.get_or_create(
                    title=cert_data['title'],
                    issuer=cert_data['issuer'],
                    defaults=cert_data
                )
                self.stdout.write(f"✅ Created certificate: {cert_data['title']}")
            except Exception as e:
                self.stdout.write(f"⚠️  MongoDB not connected for certificate: {cert_data['title']}")

        # Create CV
        self.stdout.write("Creating CV...")
        django_cv, created = DjangoCV.objects.get_or_create(
            title=cv_data['title'],
            defaults=cv_data
        )
        
        try:
            mongo_cv, created = CV.objects.get_or_create(
                title=cv_data['title'],
                defaults=cv_data
            )
            self.stdout.write("✅ Created CV")
        except:
            self.stdout.write("⚠️  MongoDB not connected for CV")

        # Create projects
        self.stdout.write("Creating projects...")
        try:
            for project_data in projects_data:
                mongo_project, created = Project.objects.get_or_create(
                    title=project_data['title'],
                    defaults=project_data
                )
                self.stdout.write(f"✅ Created project: {project_data['title']}")
        except:
            self.stdout.write("⚠️  MongoDB not connected for projects")

        self.stdout.write(
            self.style.SUCCESS(
                f'\n🎉 Successfully populated database!\n'
                f'📋 Created {len(certificates_data)} certificates\n'
                f'📄 Created 1 CV\n'
                f'🚀 Created {len(projects_data)} projects\n\n'
                f'Admin Panel: http://127.0.0.1:8001/admin/\n'
                f'Username: admin\n'
                f'Password: admin123\n'
            )
        )
