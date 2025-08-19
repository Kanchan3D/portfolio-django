# Django Portfolio with MongoDB Atlas

A comprehensive Django portfolio website for Kanchan Dasila with MongoDB Atlas integration, featuring dynamic content management and a professional admin interface.

## 🚀 Features

### Core Features
- **Dynamic Content Management**: Complete admin panel for all portfolio content
- **MongoDB Atlas Integration**: Cloud database with MongoEngine ODM
- **Single Profile System**: Streamlined profile management with automatic activation
- **Professional Admin Interface**: Custom bright blue theme with intuitive controls
- **PDF Certificate Management**: Upload and manage certificates with direct links
- **CV/Resume Management**: Dynamic CV links with version control
- **Project Showcase**: Dynamic project management with images and descriptions
- **Responsive Design**: Mobile-first design with Tailwind CSS
- **Static File Management**: Organized assets with proper directory structure

### Enhanced Admin Features
- **Bright Professional UI**: Custom blue/white admin theme
- **Single Profile Management**: Automatic profile creation and management
- **Comprehensive CRUD Operations**: Full Create, Read, Update, Delete functionality
- **Form Validation**: Built-in validation for all forms
- **Media Management**: Integrated static file handling
- **User-Friendly Interface**: Intuitive admin navigation and controls

## 📋 Portfolio Pages

- **Home Page**: Dynamic introduction with profile data and CV download
- **About Page**: Skills, education, interests from profile data
- **Projects Page**: Dynamic project showcase from database
- **My Work Page**: Professional experience and timeline
- **Certifications Page**: Dynamic certificates with PDF links
- **Contact Page**: Dynamic contact information from profile
- **Video CV Page**: Professional video introduction

## 🛠 Technologies Used

### Backend Stack
- **Django 5.2.5**: Modern Python web framework
- **MongoDB Atlas**: Cloud NoSQL database
- **MongoEngine 0.29.1**: Object Document Mapper for MongoDB
- **Python 3.11+**: Latest Python features

### Frontend Stack
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with custom properties
- **JavaScript**: Interactive features
- **Tailwind CSS**: Utility-first CSS framework
- **Font Awesome**: Professional icon library

### Database Models
- **Profile**: Personal information, contact details, social links
- **Certificate**: Educational and professional certifications
- **CV**: Resume management with versioning
- **Project**: Portfolio project showcase

## ⚙️ Installation and Setup

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd djangoPortfolio
```

### 2. Create Virtual Environment
```bash
python -m venv portfolio_env
source portfolio_env/bin/activate  # On macOS/Linux
# or
portfolio_env\Scripts\activate     # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
# MongoDB Atlas Configuration
DB_PASSWORD=your_mongodb_atlas_password

# Django Configuration
DEBUG=True
SECRET_KEY=your-django-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Optional: Custom settings
TIME_ZONE=UTC
LANGUAGE_CODE=en-us
```

### 5. MongoDB Atlas Setup
1. Create account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster (free tier available)
3. Create database user with password
4. Whitelist your IP address (0.0.0.0/0 for development)
5. Get connection string from Atlas dashboard
6. Update `DB_PASSWORD` in `.env` file

### 6. Django Setup
```bash
# Run Django migrations (for admin functionality)
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser

# Populate sample data (optional)
python manage.py populate_db
```

### 7. Start Development Server
```bash
python manage.py runserver
```

**Access Points:**
- Website: http://127.0.0.1:8000
- Admin Panel: http://127.0.0.1:8000/admin/

## 🎛 Admin Panel Guide

### Access Credentials
- **URL**: `http://127.0.0.1:8000/admin/`
- **Default Username**: admin
- **Default Password**: admin123

### Profile Management
The portfolio uses a single profile system for streamlined management:

1. **Navigate to Profile**: Admin Panel → Profile
2. **First Time Setup**: Profile is automatically created
3. **Edit Profile**: Update personal information, contact details, social links
4. **Professional Details**: Add bio, skills, location, availability status
5. **Social Media**: Instagram, LinkedIn, GitHub, and other social profiles

**Profile Fields:**
- Personal: Name, email, phone, location, bio
- Professional: Skills, profession, availability
- Social Media: Instagram, LinkedIn, GitHub, Twitter
- Media: Profile photo, background images

### Certificate Management
1. **Add Certificates**: Admin Panel → Certificates → Add Certificate
2. **Required Fields**:
   - Title: Certificate name
   - Issuer: Issuing organization
   - PDF URL: Direct link to certificate PDF
   - Description: Brief description
   - Is Featured: Display on certification page
   - Display Order: Sort order (ascending)

### CV/Resume Management
1. **Add CV**: Admin Panel → CVs → Add CV
2. **Fields**:
   - Title: Resume version title
   - PDF URL: Direct link to CV PDF
   - Version: Version number/identifier
   - Is Active: Mark as current CV (only one active)
   - Description: Version notes

### Project Management
1. **Add Projects**: Admin Panel → Projects → Add Project
2. **Project Details**:
   - Title, description, technologies used
   - GitHub repository link
   - Live demo URL
   - Project images and screenshots
   - Featured status and display order

## 📁 Project Structure

```
djangoPortfolio/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── README.md                   # Project documentation
├── .env                        # Environment variables (create this)
├── .gitignore                  # Git exclusions
├── portfolio/                  # Django project settings
│   ├── __init__.py
│   ├── settings.py             # Main configuration
│   ├── urls.py                 # Root URL patterns
│   ├── wsgi.py                 # WSGI application
│   └── asgi.py                 # ASGI application
└── main/                       # Main application
    ├── __init__.py
    ├── models.py               # MongoDB models
    ├── views.py                # View functions
    ├── admin.py                # Admin configuration
    ├── urls.py                 # App URLs
    ├── apps.py                 # App configuration
    ├── management/             # Custom management commands
    │   └── commands/
    │       └── populate_db.py  # Database population
    ├── static/                 # Static files
    │   ├── css/               # Custom stylesheets
    │   ├── js/                # JavaScript files
    │   └── assets/            # Images, icons, documents
    │       ├── icons/         # Favicon, logos, brand icons
    │       ├── project/       # Project screenshots
    │       └── Certificates/  # Certificate PDFs
    └── templates/main/         # HTML templates
        ├── base.html          # Base template
        ├── home.html          # Home page
        ├── about.html         # About page
        ├── projects.html      # Projects showcase
        ├── mywork.html        # Work experience
        ├── certification.html # Certificates
        ├── contact.html       # Contact information
        ├── videocv.html       # Video CV
        └── 404.html           # Error page
```

## 🔄 Data Flow Architecture

### 1. Admin Panel → Database
- Admin creates/edits content through Django admin
- Data validated and saved to MongoDB Atlas
- Single profile system ensures data consistency

### 2. Database → Frontend
- Views query MongoDB using MongoEngine
- Profile data fetched with intelligent fallbacks
- Templates render dynamic content

### 3. Fallback System
- Profile data: Uses defaults if database unavailable
- Static assets: Served from local files
- Error handling: Graceful degradation

## 🚀 Deployment Guide

### Environment Preparation
```bash
# Production dependencies
pip install gunicorn whitenoise

# Collect static files
python manage.py collectstatic --noinput
```

### Heroku Deployment
```bash
# Create Procfile
echo "web: gunicorn portfolio.wsgi --log-file -" > Procfile

# Initialize git
git init
git add .
git commit -m "Initial commit"

# Deploy to Heroku
heroku create your-portfolio-name
heroku config:set DEBUG=False
heroku config:set DB_PASSWORD=your_mongodb_password
heroku config:set SECRET_KEY=your_production_secret_key
git push heroku main

# Run migrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Railway Deployment
Create `railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn portfolio.wsgi"
  }
}
```

### DigitalOcean App Platform
1. Connect GitHub repository
2. Set environment variables in control panel
3. Configure build commands:
   - Build: `pip install -r requirements.txt`
   - Run: `python manage.py migrate && gunicorn portfolio.wsgi`

## 🎯 Management Commands

### Database Population
```bash
# Add sample data
python manage.py populate_db

# Clear existing data and repopulate
python manage.py populate_db --clear

# Populate specific models
python manage.py populate_db --models Certificate,Project
```

### User Management
```bash
# Create superuser
python manage.py createsuperuser

# Change user password
python manage.py changepassword username
```

### Static Files
```bash
# Collect static files for production
python manage.py collectstatic

# Clear static files cache
python manage.py collectstatic --clear
```

## 🔧 Configuration Options

### MongoDB Settings
In `portfolio/settings.py`:
```python
# Custom MongoDB configuration
MONGODB_SETTINGS = {
    'host': f'mongodb+srv://kanchan:{os.getenv("DB_PASSWORD")}@cluster0.yq5fuwe.mongodb.net/portfolio_db?retryWrites=true&w=majority',
    'connect': False,
}
```

### Static Files Configuration
```python
# Static files settings
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'main/static'),
]
```

### Admin Interface Customization
```python
# Custom admin settings
ADMIN_SITE_HEADER = "Portfolio Admin"
ADMIN_SITE_TITLE = "Portfolio Admin Portal"
ADMIN_INDEX_TITLE = "Welcome to Portfolio Administration"
```

## 🔐 Security Best Practices

### Environment Security
1. **Never commit sensitive data**: Use `.env` for credentials
2. **Strong passwords**: Use complex database and admin passwords
3. **Environment isolation**: Separate development/production settings
4. **HTTPS in production**: Always use SSL certificates

### Database Security
1. **MongoDB Atlas**: Use IP whitelisting in production
2. **User permissions**: Create database users with minimal required permissions
3. **Connection encryption**: MongoDB Atlas uses encryption by default
4. **Regular backups**: Enable automatic backups

### Django Security
```python
# Production security settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

## 🐛 Troubleshooting

### Common Issues

#### MongoDB Connection Errors
```bash
# Check environment variables
echo $DB_PASSWORD

# Test MongoDB connection
python -c "import mongoengine; mongoengine.connect('portfolio_db', host='your_connection_string')"
```

#### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic

# Check STATIC_URL in settings
# Ensure static files are in correct directories
```

#### Admin Panel Access Issues
```bash
# Create new superuser
python manage.py createsuperuser

# Reset admin password
python manage.py changepassword admin
```

### Debug Mode
Enable detailed error messages in development:
```python
# In settings.py
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
```

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Set up development environment
4. Make changes with tests
5. Submit pull request

### Code Standards
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings for functions
- Write unit tests for new features
- Update documentation

### Testing
```bash
# Run Django tests
python manage.py test

# Check code quality
flake8 .
black --check .
```

## 📞 Support & Contact

### Technical Support
- **Documentation**: Check this README and inline comments
- **Issues**: Create GitHub issue with detailed description
- **Questions**: Contact via email or LinkedIn

### Contact Information
- **Developer**: Kanchan Dasila
- **Email**: kanchandasila31@gmail.com
- **GitHub**: [Kanchan3D](https://github.com/Kanchan3D)
- **LinkedIn**: [kanchan-dasila](https://linkedin.com/in/kanchan-dasila)
- **Portfolio**: [Live Demo](https://your-portfolio-url.com)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ❌ Liability
- ❌ Warranty

---

## 🎉 Quick Start Checklist

### Initial Setup
- [ ] Clone repository and create virtual environment
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Create `.env` file with MongoDB credentials
- [ ] Set up MongoDB Atlas cluster and database
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`

### Data Setup
- [ ] Populate sample data: `python manage.py populate_db`
- [ ] Access admin panel: http://127.0.0.1:8000/admin/
- [ ] Configure profile information
- [ ] Add certificates and CV
- [ ] Upload project information

### Launch
- [ ] Start development server: `python manage.py runserver`
- [ ] View website: http://127.0.0.1:8000/
- [ ] Test all pages and functionality
- [ ] Verify admin panel operations

### Production Deployment
- [ ] Set up production environment variables
- [ ] Configure static files for production
- [ ] Deploy to chosen platform (Heroku, Railway, etc.)
- [ ] Set up domain and SSL certificate
- [ ] Test production deployment

**🚀 Your Django portfolio is ready to showcase your professional journey!**

---

*Built with ❤️ using Django and MongoDB Atlas*
