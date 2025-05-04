from django.urls import path
from . import views
from .views import analyze_image  # Make sure this is imported

urlpatterns = [
    path('home/', views.HomePage, name='home'),
    path('signup/', views.SignupPage, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('Image/', views.image_analysis, name='image_analysis'),
    path('Video/', views.video_analysis, name='video_analysis'),
    path('upload-image/', views.image_upload, name='image_upload'),
    
    # Add the new URL pattern for the analyze_image view
    path('analyze/', analyze_image, name='analyze'),  # New path added
]
