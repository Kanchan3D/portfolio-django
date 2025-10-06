from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
    path('mywork/', views.mywork, name='mywork'),
    path('certification/', views.certification, name='certification'),
    path('api/profile/', views.profile_api, name='profile_api'),
    path('api/contact/', views.contact_submit, name='contact_submit'),
    # Test route to preview 404 page in development
    path('test-404/', views.custom_404_view, name='test_404'),
]
