"""
Django management command to populate MongoDB with initial portfolio data
"""

from django.core.management.base import BaseCommand
from main.models import Certificate, CV, Project
from datetime import date, datetime

class Command(BaseCommand):
    help = 'Populate MongoDB with initial portfolio data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting MongoDB data population...'))
        
        # Clear existing data
        try:
            Certificate.objects.delete()
            CV.objects.delete()
            Project.objects.delete()
            self.stdout.write(self.style.WARNING('Cleared existing data'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not clear existing data: {e}'))

        # Add sample certificates
        certificates = [
            {
                'title': 'Advanced JavaScript',
                'issuer': 'FreeCodeCamp',
                'description': 'Advanced concepts in JavaScript programming including closures, async/await, and ES6+ features',
                'pdf_url': 'https://example.com/certificates/advanced-javascript.pdf',
                'issue_date': date(2023, 6, 15),
                'is_featured': True,
                'display_order': 1
            },
            {
                'title': 'Advanced React',
                'issuer': 'FreeCodeCamp',
                'description': 'Advanced React development techniques including hooks, context API, and performance optimization',
                'pdf_url': 'https://example.com/certificates/advanced-react.pdf',
                'issue_date': date(2023, 7, 20),
                'is_featured': True,
                'display_order': 2
            },
            {
                'title': 'Node.js Development',
                'issuer': 'Online Course',
                'description': 'Complete Node.js backend development including Express.js, MongoDB, and RESTful APIs',
                'pdf_url': 'https://example.com/certificates/nodejs-development.pdf',
                'issue_date': date(2023, 8, 10),
                'is_featured': True,
                'display_order': 3
            },
            {
                'title': 'TypeScript Mastery',
                'issuer': 'Online Course',
                'description': 'TypeScript programming language fundamentals and advanced features',
                'pdf_url': 'https://example.com/certificates/typescript-mastery.pdf',
                'issue_date': date(2023, 9, 5),
                'is_featured': True,
                'display_order': 4
            },
            {
                'title': 'Next.js Framework',
                'issuer': 'Online Course',
                'description': 'Next.js React framework for production-ready applications',
                'pdf_url': 'https://example.com/certificates/nextjs-framework.pdf',
                'issue_date': date(2023, 10, 12),
                'is_featured': True,
                'display_order': 5
            },
            {
                'title': 'Express.js Backend',
                'issuer': 'Online Course',
                'description': 'Express.js framework for Node.js backend development',
                'pdf_url': 'https://example.com/certificates/expressjs-backend.pdf',
                'issue_date': date(2023, 11, 8),
                'is_featured': True,
                'display_order': 6
            }
        ]

        cert_count = 0
        for cert_data in certificates:
            try:
                cert = Certificate(**cert_data)
                cert.save()
                cert_count += 1
                self.stdout.write(f'✓ Added certificate: {cert_data["title"]}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Failed to add certificate {cert_data["title"]}: {e}'))

        # Add sample projects
        projects = [
            {
                'title': 'E-Commerce Platform',
                'description': 'Full-stack e-commerce application with React frontend, Node.js backend, and MongoDB database. Features include user authentication, product catalog, shopping cart, and payment integration.',
                'image_url': 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400',
                'technologies': 'React, Node.js, MongoDB, Express, Stripe, JWT',
                'github_url': 'https://github.com/kanchandasila/ecommerce-platform',
                'live_url': 'https://ecommerce-demo.vercel.app',
                'is_featured': True
            },
            {
                'title': 'Task Management System',
                'description': 'A collaborative task management application built with React and Django. Features real-time updates, team collaboration, and project tracking.',
                'image_url': 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=400',
                'technologies': 'React, Django, PostgreSQL, WebSockets, Redis',
                'github_url': 'https://github.com/kanchandasila/task-manager',
                'live_url': 'https://taskmanager-demo.herokuapp.com',
                'is_featured': True
            },
            {
                'title': 'URL Shortener Service',
                'description': 'URL shortening service with analytics dashboard. Built with Node.js and MongoDB, featuring custom domains and click tracking.',
                'image_url': 'https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?w=400',
                'technologies': 'Node.js, Express, MongoDB, Chart.js, JWT',
                'github_url': 'https://github.com/kanchandasila/url-shortener',
                'live_url': 'https://shorturl-service.vercel.app',
                'is_featured': True
            },
            {
                'title': 'LeetCode Analytics Dashboard',
                'description': 'Personal dashboard to track LeetCode problem-solving progress with data visualization and performance metrics.',
                'image_url': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400',
                'technologies': 'React, Chart.js, LeetCode API, Local Storage',
                'github_url': 'https://github.com/kanchandasila/leetmetric',
                'live_url': 'https://leetmetric.netlify.app',
                'is_featured': True
            },
            {
                'title': 'Learning Management System',
                'description': 'Complete LMS with course management, student enrollment, progress tracking, and video streaming capabilities.',
                'image_url': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=400',
                'technologies': 'React, Node.js, MySQL, AWS S3, Video.js',
                'github_url': 'https://github.com/kanchandasila/lms-platform',
                'live_url': 'https://lms-demo.herokuapp.com',
                'is_featured': True
            },
            {
                'title': 'Blockchain Voting System',
                'description': 'Secure digital voting system using blockchain technology for transparency and immutability.',
                'image_url': 'https://images.unsplash.com/photo-1559526324-4b87b5e36e44?w=400',
                'technologies': 'React, Solidity, Web3.js, Ethereum, MetaMask',
                'github_url': 'https://github.com/kanchandasila/blockchain-voting',
                'live_url': 'https://voting-dapp.netlify.app',
                'is_featured': True
            }
        ]

        project_count = 0
        for proj_data in projects:
            try:
                project = Project(**proj_data)
                project.save()
                project_count += 1
                self.stdout.write(f'✓ Added project: {proj_data["title"]}')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Failed to add project {proj_data["title"]}: {e}'))

        # Add sample CV
        try:
            cv = CV(
                title='Kanchan Dasila - Software Developer Resume',
                pdf_url='https://drive.google.com/file/d/1yzdrXJG6MOCjmjz1-GzCCpPxSefCiVT3/view',
                version='2.0',
                is_active=True,
                description='Latest resume showcasing full-stack development skills and project experience'
            )
            cv.save()
            self.stdout.write(f'✓ Added CV: {cv.title}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Failed to add CV: {e}'))

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated MongoDB!\n'
                f'- {cert_count} certificates added\n'
                f'- {project_count} projects added\n'
                f'- 1 CV added\n'
                f'Your portfolio is now ready with MongoDB Atlas!'
            )
        )
